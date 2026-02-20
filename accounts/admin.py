"""Admin configuration for the accounts app."""

from django.contrib import admin
from .models import StudentProfile, AuditLog


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin interface for managing student profiles."""
    list_display = [
        'user', 'student_id', 'year_group', 'role', 'is_eligible'
    ]
    list_filter = ['role', 'year_group', 'is_eligible']
    search_fields = [
        'user__username', 'user__first_name',
        'user__last_name', 'student_id'
    ]
    list_editable = ['is_eligible', 'role']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for viewing audit logs (read-only)."""
    list_display = [
        'user', 'action', 'description', 'timestamp'
    ]
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = [
        'user', 'action', 'description', 'target_model',
        'target_id', 'ip_address', 'timestamp'
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False