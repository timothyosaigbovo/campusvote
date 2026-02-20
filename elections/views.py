"""
Views for the elections app.

Handles the student-facing features: home page, dashboard,
election browsing, candidate profiles, voting with duplicate
prevention, and results display.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from .models import Election, Position, Candidate, Vote


def home_view(request):
    """
    Public home page displaying active and upcoming elections.
    Accessible to all users without login.
    """
    active_elections = Election.objects.filter(status='active')
    upcoming_elections = Election.objects.filter(
        status='draft'
    ).order_by('start_date')[:5]
    closed_elections = Election.objects.filter(
        status='closed', results_published=True
    ).order_by('-end_date')[:5]

    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'closed_elections': closed_elections,
    }
    return render(request, 'elections/home.html', context)


@login_required
def dashboard_view(request):
    """
    Student dashboard showing election status and voting progress.
    Displays active, upcoming, and closed elections relevant
    to the student's year group.
    """
    profile = request.user.profile
    year_group = profile.year_group

    # Get elections where student's year group is eligible
    all_elections = Election.objects.all()

    active_elections = []
    upcoming_elections = []
    closed_elections = []

    for election in all_elections:
        eligible_groups = election.get_eligible_year_groups_list()
        if year_group in eligible_groups:
            # Calculate voting progress
            positions = election.positions.all()
            total_positions = positions.count()
            voted_positions = Vote.objects.filter(
                student_profile=profile,
                position__election=election
            ).count()

            election.total_positions = total_positions
            election.voted_positions = voted_positions
            election.voting_complete = (
                voted_positions >= total_positions
                and total_positions > 0
            )

            if total_positions > 0:
                election.progress_percentage = int(
                    (voted_positions / total_positions) * 100
                )
            else:
                election.progress_percentage = 0

            if election.status == 'active':
                active_elections.append(election)
            elif election.status == 'draft':
                upcoming_elections.append(election)
            elif election.status in ('closed', 'archived'):
                closed_elections.append(election)

    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'closed_elections': closed_elections,
        'profile': profile,
    }
    return render(request, 'elections/dashboard.html', context)


@login_required
def election_detail_view(request, pk):
    """
    Display election details with positions and candidates.
    Shows voting status for each position.
    """
    election = get_object_or_404(Election, pk=pk)
    profile = request.user.profile

    # Check eligibility
    if not election.is_student_eligible(profile):
        messages.warning(
            request,
            'You are not eligible to vote in this election.'
        )

    positions = election.positions.all().prefetch_related(
        'candidates', 'candidates__student_profile',
        'candidates__student_profile__user'
    )

    # Check which positions the student has voted for
    voted_position_ids = Vote.objects.filter(
        student_profile=profile,
        position__election=election
    ).values_list('position_id', flat=True)

    position_data = []
    for position in positions:
        position_data.append({
            'position': position,
            'candidates': position.candidates.filter(
                is_approved=True
            ),
            'has_voted': position.id in voted_position_ids,
        })

    context = {
        'election': election,
        'position_data': position_data,
        'voted_position_ids': list(voted_position_ids),
    }
    return render(
        request, 'elections/election_detail.html', context
    )


@login_required
def candidate_detail_view(request, pk):
    """Display detailed candidate profile and manifesto."""
    candidate = get_object_or_404(
        Candidate.objects.select_related(
            'student_profile', 'student_profile__user',
            'position', 'position__election'
        ),
        pk=pk,
        is_approved=True
    )
    context = {'candidate': candidate}
    return render(
        request, 'elections/candidate_detail.html', context
    )


@login_required
def cast_vote_view(request, position_id):
    """
    Handle vote casting with three layers of protection:
    1. UI-level: hide vote button if already voted
    2. View-level: check before processing
    3. Database-level: UniqueConstraint prevents duplicates

    Shows confirmation before recording the vote.
    """
    position = get_object_or_404(
        Position.objects.select_related('election'),
        pk=position_id
    )
    election = position.election
    profile = request.user.profile

    # Check election is active
    if not election.is_active:
        messages.error(
            request, 'This election is not currently active.'
        )
        return redirect(
            'elections:election_detail', pk=election.pk
        )

    # Check eligibility
    if not election.is_student_eligible(profile):
        messages.error(
            request, 'You are not eligible to vote in this election.'
        )
        return redirect(
            'elections:election_detail', pk=election.pk
        )

    # Check if already voted (view-level protection)
    existing_vote = Vote.objects.filter(
        student_profile=profile, position=position
    ).exists()

    if existing_vote:
        messages.warning(
            request,
            f'You have already voted for {position.title}.'
        )
        return redirect(
            'elections:election_detail', pk=election.pk
        )

    candidates = position.candidates.filter(
        is_approved=True
    ).select_related('student_profile', 'student_profile__user')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        if not candidate_id:
            messages.error(
                request, 'Please select a candidate.'
            )
            return render(request, 'elections/cast_vote.html', {
                'position': position,
                'election': election,
                'candidates': candidates,
            })

        candidate = get_object_or_404(
            Candidate, pk=candidate_id,
            position=position, is_approved=True
        )

        # Database-level protection with try/except
        try:
            Vote.objects.create(
                student_profile=profile,
                position=position,
                candidate=candidate
            )
            messages.success(
                request,
                f'Your vote for {position.title} has been '
                f'recorded successfully!'
            )
        except IntegrityError:
            messages.error(
                request,
                f'You have already voted for {position.title}. '
                f'Duplicate votes are not allowed.'
            )

        return redirect(
            'elections:election_detail', pk=election.pk
        )

    context = {
        'position': position,
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'elections/cast_vote.html', context)


@login_required
def results_view(request, pk):
    """
    Display election results with vote counts and percentages.
    Only accessible when results have been published.
    """
    election = get_object_or_404(Election, pk=pk)

    if not election.results_published:
        messages.info(
            request,
            'Results for this election have not been '
            'published yet.'
        )
        return redirect('elections:dashboard')

    positions = election.positions.all()
    results_data = []

    for position in positions:
        candidates = position.candidates.filter(
            is_approved=True
        ).select_related(
            'student_profile', 'student_profile__user'
        )

        total_votes = position.total_votes()
        candidate_results = []

        for candidate in candidates:
            votes = candidate.vote_count()
            percentage = (
                round((votes / total_votes) * 100, 1)
                if total_votes > 0 else 0
            )
            candidate_results.append({
                'candidate': candidate,
                'votes': votes,
                'percentage': percentage,
            })

        # Sort by votes descending
        candidate_results.sort(
            key=lambda x: x['votes'], reverse=True
        )

        # Mark the winner
        if candidate_results and candidate_results[0]['votes'] > 0:
            candidate_results[0]['is_winner'] = True

        results_data.append({
            'position': position,
            'total_votes': total_votes,
            'candidate_results': candidate_results,
        })

    context = {
        'election': election,
        'results_data': results_data,
    }
    return render(request, 'elections/results.html', context)


def custom_404(request, exception):
    """Custom 404 error page."""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page."""
    return render(request, 'errors/500.html', status=500)