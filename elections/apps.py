"""App configuration for the elections app."""

from django.apps import AppConfig


class ElectionsConfig(AppConfig):
    """Configuration for the elections application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elections'
    verbose_name = 'Elections'