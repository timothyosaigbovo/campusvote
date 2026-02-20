"""App configuration for the management app."""

from django.apps import AppConfig


class ManagementConfig(AppConfig):
    """Configuration for the management application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'
    verbose_name = 'Election Management'