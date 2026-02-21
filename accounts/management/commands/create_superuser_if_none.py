"""
Management command to create or promote admin users
for production deployment.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import StudentProfile


class Command(BaseCommand):
    help = 'Create superuser and promote to admin role'

    def handle(self, *args, **options):
        # Promote existing user if DJANGO_SU_NAME matches
        username = os.environ.get('DJANGO_SU_NAME', 'admin')
        password = os.environ.get('DJANGO_SU_PASSWORD', '')
        email = os.environ.get(
            'DJANGO_SU_EMAIL', 'admin@campusvote.com'
        )

        try:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            if password:
                user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Promoted "{username}" to superuser.'
                )
            )
        except User.DoesNotExist:
            if not password:
                self.stdout.write(
                    self.style.ERROR(
                        'Set DJANGO_SU_PASSWORD env variable.'
                    )
                )
                return
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created superuser "{username}".'
                )
            )

        # Set admin role on profile
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.role = 'admin'
            profile.student_id = profile.student_id or 'STU00001'
            profile.save()
            self.stdout.write(
                self.style.SUCCESS('Admin role set.')
            )