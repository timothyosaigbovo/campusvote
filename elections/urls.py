"""URL configuration for the elections app."""

from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path(
        '',
        views.home_view,
        name='home'
    ),
    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),
    path(
        'election/<int:pk>/',
        views.election_detail_view,
        name='election_detail'
    ),
    path(
        'candidate/<int:pk>/',
        views.candidate_detail_view,
        name='candidate_detail'
    ),
    path(
        'vote/<int:position_id>/',
        views.cast_vote_view,
        name='cast_vote'
    ),
    path(
        'results/<int:pk>/',
        views.results_view,
        name='results'
    ),
]