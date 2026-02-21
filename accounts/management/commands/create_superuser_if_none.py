"""
Management command to create an initial superuser
for production deployment where shell access
is not available.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import StudentProfile


class Command(BaseCommand):
    help = 'Create a superuser with admin profile if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superuser already exists.')
            )
            return

        username = os.environ.get('DJANGO_SU_NAME', 'admin')
        email = os.environ.get('DJANGO_SU_EMAIL', 'admin@campusvote.com')
        password = os.environ.get('DJANGO_SU_PASSWORD', '')

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    'Set DJANGO_SU_PASSWORD environment variable.'
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        profile = user.profile
        profile.role = 'admin'
        profile.student_id = 'STU00001'
        profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" created with admin role.'
            )
        )