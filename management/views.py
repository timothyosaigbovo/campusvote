"""
Views for the management app.

Provides admin CRUD operations for elections, positions,
candidates, and voter management. Includes analytics
dashboard, CSV export, and comprehensive audit logging.
"""

import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from elections.models import Election, Position, Candidate, Vote
from accounts.models import StudentProfile, AuditLog
from .decorators import admin_required, admin_or_observer_required
from .forms import (
    ElectionForm,
    PositionForm,
    CandidateForm,
    VoterEligibilityForm,
)


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def log_action(request, action, description, target_model='',
               target_id=None):
    """Create an audit log entry."""
    AuditLog.objects.create(
        user=request.user,
        action=action,
        description=description,
        target_model=target_model,
        target_id=target_id,
        ip_address=get_client_ip(request),
    )


# ── Dashboard ───────────────────────────────────

@admin_required
def admin_dashboard_view(request):
    """Admin dashboard with summary statistics."""
    total_elections = Election.objects.count()
    active_elections = Election.objects.filter(
        status='active'
    ).count()
    total_candidates = Candidate.objects.count()
    total_votes = Vote.objects.count()
    total_students = StudentProfile.objects.filter(
        role='student'
    ).count()

    recent_logs = AuditLog.objects.all()[:10]

    context = {
        'total_elections': total_elections,
        'active_elections': active_elections,
        'total_candidates': total_candidates,
        'total_votes': total_votes,
        'total_students': total_students,
        'recent_logs': recent_logs,
    }
    return render(
        request, 'management/dashboard.html', context
    )


# ── Election CRUD ───────────────────────────────

@admin_required
def election_list_view(request):
    """List all elections with status filters."""
    elections = Election.objects.all().annotate(
        position_count=Count('positions'),
        candidate_count=Count('positions__candidates'),
    )
    context = {'elections': elections}
    return render(
        request, 'management/election_list.html', context
    )


@admin_required
def election_create_view(request):
    """Create a new election."""
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save()
            log_action(
                request, 'create',
                f'Created election: {election.title}',
                'Election', election.pk
            )
            messages.success(
                request,
                f'Election "{election.title}" created '
                f'successfully.'
            )
            return redirect(
                'management:election_detail', pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ElectionForm()

    context = {'form': form, 'action': 'Create'}
    return render(
        request, 'management/election_form.html', context
    )


@admin_required
def election_detail_view(request, pk):
    """View election details with positions and candidates."""
    election = get_object_or_404(Election, pk=pk)
    positions = election.positions.all().prefetch_related(
        'candidates', 'candidates__student_profile',
        'candidates__student_profile__user'
    )
    context = {
        'election': election,
        'positions': positions,
    }
    return render(
        request, 'management/election_detail.html', context
    )


@admin_required
def election_update_view(request, pk):
    """Update an existing election."""
    election = get_object_or_404(Election, pk=pk)

    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            election = form.save()
            log_action(
                request, 'update',
                f'Updated election: {election.title}',
                'Election', election.pk
            )
            messages.success(
                request,
                f'Election "{election.title}" updated '
                f'successfully.'
            )
            return redirect(
                'management:election_detail', pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ElectionForm(instance=election)

    context = {
        'form': form,
        'action': 'Update',
        'election': election,
    }
    return render(
        request, 'management/election_form.html', context
    )


@admin_required
def election_delete_view(request, pk):
    """Delete an election with confirmation."""
    election = get_object_or_404(Election, pk=pk)

    if request.method == 'POST':
        title = election.title
        election_id = election.pk
        election.delete()
        log_action(
            request, 'delete',
            f'Deleted election: {title}',
            'Election', election_id
        )
        messages.success(
            request,
            f'Election "{title}" has been deleted.'
        )
        return redirect('management:election_list')

    context = {'election': election}
    return render(
        request,
        'management/election_confirm_delete.html',
        context
    )


# ── Position CRUD ───────────────────────────────

@admin_required
def position_create_view(request, election_pk):
    """Create a new position within an election."""
    election = get_object_or_404(Election, pk=election_pk)

    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.election = election
            position.save()
            log_action(
                request, 'create',
                f'Created position: {position.title} '
                f'in {election.title}',
                'Position', position.pk
            )
            messages.success(
                request,
                f'Position "{position.title}" created '
                f'successfully.'
            )
            return redirect(
                'management:election_detail',
                pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = PositionForm()

    context = {
        'form': form,
        'election': election,
        'action': 'Create',
    }
    return render(
        request, 'management/position_form.html', context
    )


@admin_required
def position_update_view(request, pk):
    """Update an existing position."""
    position = get_object_or_404(Position, pk=pk)
    election = position.election

    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save()
            log_action(
                request, 'update',
                f'Updated position: {position.title}',
                'Position', position.pk
            )
            messages.success(
                request,
                f'Position "{position.title}" updated '
                f'successfully.'
            )
            return redirect(
                'management:election_detail',
                pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = PositionForm(instance=position)

    context = {
        'form': form,
        'election': election,
        'action': 'Update',
        'position': position,
    }
    return render(
        request, 'management/position_form.html', context
    )


@admin_required
def position_delete_view(request, pk):
    """Delete a position with confirmation."""
    position = get_object_or_404(Position, pk=pk)
    election = position.election

    if request.method == 'POST':
        title = position.title
        position_id = position.pk
        position.delete()
        log_action(
            request, 'delete',
            f'Deleted position: {title}',
            'Position', position_id
        )
        messages.success(
            request,
            f'Position "{title}" has been deleted.'
        )
        return redirect(
            'management:election_detail', pk=election.pk
        )

    context = {
        'position': position,
        'election': election,
    }
    return render(
        request,
        'management/position_confirm_delete.html',
        context
    )


# ── Candidate CRUD ──────────────────────────────

@admin_required
def candidate_create_view(request, position_pk):
    """Create a new candidate for a position."""
    position = get_object_or_404(Position, pk=position_pk)
    election = position.election

    if request.method == 'POST':
        form = CandidateForm(
            request.POST, request.FILES, position=position
        )
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.position = position
            candidate.save()
            log_action(
                request, 'create',
                f'Created candidate: '
                f'{candidate.student_profile} '
                f'for {position.title}',
                'Candidate', candidate.pk
            )
            messages.success(
                request,
                f'Candidate added to "{position.title}" '
                f'successfully.'
            )
            return redirect(
                'management:election_detail',
                pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = CandidateForm(position=position)

    context = {
        'form': form,
        'position': position,
        'election': election,
        'action': 'Add',
    }
    return render(
        request, 'management/candidate_form.html', context
    )


@admin_required
def candidate_update_view(request, pk):
    """Update an existing candidate."""
    candidate = get_object_or_404(Candidate, pk=pk)
    position = candidate.position
    election = position.election

    if request.method == 'POST':
        form = CandidateForm(
            request.POST, request.FILES,
            instance=candidate, position=position
        )
        if form.is_valid():
            candidate = form.save()
            log_action(
                request, 'update',
                f'Updated candidate: '
                f'{candidate.student_profile}',
                'Candidate', candidate.pk
            )
            messages.success(
                request,
                'Candidate updated successfully.'
            )
            return redirect(
                'management:election_detail',
                pk=election.pk
            )
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = CandidateForm(
            instance=candidate, position=position
        )

    context = {
        'form': form,
        'position': position,
        'election': election,
        'action': 'Update',
        'candidate': candidate,
    }
    return render(
        request, 'management/candidate_form.html', context
    )


@admin_required
def candidate_delete_view(request, pk):
    """Delete a candidate with confirmation."""
    candidate = get_object_or_404(Candidate, pk=pk)
    position = candidate.position
    election = position.election

    if request.method == 'POST':
        name = str(candidate.student_profile)
        candidate_id = candidate.pk
        candidate.delete()
        log_action(
            request, 'delete',
            f'Deleted candidate: {name}',
            'Candidate', candidate_id
        )
        messages.success(
            request,
            f'Candidate "{name}" has been removed.'
        )
        return redirect(
            'management:election_detail', pk=election.pk
        )

    context = {
        'candidate': candidate,
        'position': position,
        'election': election,
    }
    return render(
        request,
        'management/candidate_confirm_delete.html',
        context
    )


# ── Voter Management ────────────────────────────

@admin_required
def voter_list_view(request):
    """List all students with eligibility management."""
    students = StudentProfile.objects.filter(
        role='student'
    ).select_related('user')

    # Handle eligibility toggle
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        if profile_id:
            profile = get_object_or_404(
                StudentProfile, pk=profile_id
            )
            profile.is_eligible = not profile.is_eligible
            profile.save()

            status = (
                'eligible' if profile.is_eligible
                else 'suspended'
            )
            log_action(
                request, 'eligibility',
                f'Changed eligibility for '
                f'{profile.user.get_full_name()}: {status}',
                'StudentProfile', profile.pk
            )
            messages.success(
                request,
                f'{profile.user.get_full_name()} is now '
                f'{status}.'
            )
            return redirect('management:voter_list')

    context = {'students': students}
    return render(
        request, 'management/voter_list.html', context
    )


# ── Analytics ───────────────────────────────────

@admin_or_observer_required
def analytics_view(request, pk):
    """
    Display election analytics with turnout data
    by year group and vote distribution charts.
    """
    election = get_object_or_404(Election, pk=pk)
    positions = election.positions.all()

    # Calculate turnout by year group
    eligible_groups = election.get_eligible_year_groups_list()
    turnout_data = []

    for year_group in eligible_groups:
        eligible_count = StudentProfile.objects.filter(
            year_group=year_group,
            role='student',
            is_eligible=True,
        ).count()

        voted_count = Vote.objects.filter(
            position__election=election,
            student_profile__year_group=year_group,
        ).values(
            'student_profile'
        ).distinct().count()

        percentage = (
            round((voted_count / eligible_count) * 100, 1)
            if eligible_count > 0 else 0
        )

        turnout_data.append({
            'year_group': year_group,
            'year_group_display': dict(
                StudentProfile.YEAR_GROUP_CHOICES
            ).get(year_group, year_group),
            'eligible': eligible_count,
            'voted': voted_count,
            'percentage': percentage,
        })

    # Position results
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

    # Overall stats
    total_eligible = StudentProfile.objects.filter(
        role='student',
        is_eligible=True,
        year_group__in=eligible_groups,
    ).count()

    total_voted = Vote.objects.filter(
        position__election=election,
    ).values(
        'student_profile'
    ).distinct().count()

    overall_turnout = (
        round((total_voted / total_eligible) * 100, 1)
        if total_eligible > 0 else 0
    )

    context = {
        'election': election,
        'turnout_data': turnout_data,
        'results_data': results_data,
        'total_eligible': total_eligible,
        'total_voted': total_voted,
        'overall_turnout': overall_turnout,
        'position_count': positions.count(),
    }
    return render(
        request, 'management/analytics.html', context
    )


# ── CSV Export ──────────────────────────────────

@admin_required
def export_results_csv(request, pk):
    """Export election results as a CSV file."""
    election = get_object_or_404(Election, pk=pk)

    response = HttpResponse(
        content_type='text/csv; charset=utf-8-sig'
    )
    response['Content-Disposition'] = (
        f'attachment; filename='
        f'"results_{election.pk}.csv"'
    )

    # UTF-8 BOM for Excel compatibility
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'Position', 'Candidate', 'Year Group',
        'Votes', 'Percentage'
    ])

    for position in election.positions.all():
        total_votes = position.total_votes()
        for candidate in position.candidates.filter(
            is_approved=True
        ):
            votes = candidate.vote_count()
            percentage = (
                round((votes / total_votes) * 100, 1)
                if total_votes > 0 else 0
            )
            writer.writerow([
                position.title,
                candidate.student_profile.user.get_full_name(),
                candidate.student_profile.get_year_group_display(),
                votes,
                f'{percentage}%',
            ])

    log_action(
        request, 'export',
        f'Exported results CSV for: {election.title}',
        'Election', election.pk
    )

    return response


# ── Audit Logs ──────────────────────────────────

@admin_required
def audit_logs_view(request):
    """Display audit log with filtering."""
    logs = AuditLog.objects.all().select_related('user')[:100]

    # Filter by action type
    action_filter = request.GET.get('action')
    if action_filter:
        logs = logs.filter(action=action_filter)

    context = {
        'logs': logs,
        'action_choices': AuditLog.ACTION_CHOICES,
        'current_filter': action_filter,
    }
    return render(
        request, 'management/audit_logs.html', context
    )