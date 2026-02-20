"""URL configuration for the management app."""

from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # Dashboard
    path(
        '',
        views.admin_dashboard_view,
        name='dashboard'
    ),

    # Election CRUD
    path(
        'elections/',
        views.election_list_view,
        name='election_list'
    ),
    path(
        'elections/create/',
        views.election_create_view,
        name='election_create'
    ),
    path(
        'elections/<int:pk>/',
        views.election_detail_view,
        name='election_detail'
    ),
    path(
        'elections/<int:pk>/edit/',
        views.election_update_view,
        name='election_update'
    ),
    path(
        'elections/<int:pk>/delete/',
        views.election_delete_view,
        name='election_delete'
    ),

    # Position CRUD
    path(
        'elections/<int:election_pk>/positions/create/',
        views.position_create_view,
        name='position_create'
    ),
    path(
        'positions/<int:pk>/edit/',
        views.position_update_view,
        name='position_update'
    ),
    path(
        'positions/<int:pk>/delete/',
        views.position_delete_view,
        name='position_delete'
    ),

    # Candidate CRUD
    path(
        'positions/<int:position_pk>/candidates/create/',
        views.candidate_create_view,
        name='candidate_create'
    ),
    path(
        'candidates/<int:pk>/edit/',
        views.candidate_update_view,
        name='candidate_update'
    ),
    path(
        'candidates/<int:pk>/delete/',
        views.candidate_delete_view,
        name='candidate_delete'
    ),

    # Voter Management
    path(
        'voters/',
        views.voter_list_view,
        name='voter_list'
    ),

    # Analytics
    path(
        'elections/<int:pk>/analytics/',
        views.analytics_view,
        name='analytics'
    ),

    # CSV Export
    path(
        'elections/<int:pk>/export/',
        views.export_results_csv,
        name='export_csv'
    ),

    # Audit Logs
    path(
        'audit-logs/',
        views.audit_logs_view,
        name='audit_logs'
    ),
]