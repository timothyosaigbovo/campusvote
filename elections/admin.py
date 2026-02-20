"""Admin configuration for the elections app."""

from django.contrib import admin
from .models import Election, Position, Candidate, Vote


class PositionInline(admin.TabularInline):
    """Inline display of positions within election admin."""
    model = Position
    extra = 1


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    """Admin interface for managing elections."""
    list_display = [
        'title', 'status', 'start_date', 'end_date',
        'results_published'
    ]
    list_filter = ['status', 'results_published']
    search_fields = ['title', 'description']
    inlines = [PositionInline]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin interface for managing positions."""
    list_display = [
        'title', 'election', 'display_order', 'max_candidates'
    ]
    list_filter = ['election']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """Admin interface for managing candidates."""
    list_display = [
        'student_profile', 'position', 'is_approved'
    ]
    list_filter = ['is_approved', 'position__election']
    search_fields = [
        'student_profile__user__first_name',
        'student_profile__user__last_name'
    ]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin interface for viewing votes (read-only)."""
    list_display = [
        'student_profile', 'position', 'candidate', 'cast_at'
    ]
    list_filter = ['position__election', 'position']
    readonly_fields = [
        'student_profile', 'position', 'candidate', 'cast_at'
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False