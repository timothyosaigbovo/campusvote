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
    to the student's year group. Admins see all elections.
    """
    profile = request.user.profile
    year_group = profile.year_group
    is_admin = profile.role == 'admin'

    # Get elections — admins see all, students see eligible only
    all_elections = Election.objects.all()

    active_elections = []
    upcoming_elections = []
    closed_elections = []

    for election in all_elections:
        eligible_groups = election.get_eligible_year_groups_list()
        if is_admin or year_group in eligible_groups:
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



@login_required
def results_view(request, pk):
    """
    Display published results for a closed election.
    Shows vote counts and percentages per candidate,
    grouped by position.
    """
    election = get_object_or_404(Election, pk=pk)

    # Guard: only show results if they've been published
    if not election.results_published:
        messages.error(
            request,
            'Results for this election have not been '
            'published yet.'
        )
        return redirect('elections:dashboard')

    positions = election.positions.all().prefetch_related(
        'candidates',
        'candidates__student_profile',
        'candidates__student_profile__user',
    )

    results_data = []
    for position in positions:
        candidates = position.candidates.filter(
            is_approved=True
        ).select_related(
            'student_profile', 'student_profile__user'
        )
        total_votes = position.total_votes()

        candidate_data = []
        for candidate in candidates:
            votes = candidate.vote_count()
            percentage = (
                round((votes / total_votes) * 100, 1)
                if total_votes > 0 else 0
            )
            candidate_data.append({
                'candidate': candidate,
                'votes': votes,
                'percentage': percentage,
            })

        candidate_data.sort(
            key=lambda x: x['votes'], reverse=True
        )

        results_data.append({
            'position': position,
            'total_votes': total_votes,
            'candidates': candidate_data,
        })

    context = {
        'election': election,
        'results_data': results_data,
    }
    return render(
        request, 'elections/results.html', context
    )