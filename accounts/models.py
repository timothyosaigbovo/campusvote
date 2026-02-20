"""
Models for the accounts app.

Defines the StudentProfile model extending Django's User model
with student-specific fields, and the AuditLog model for
tracking all administrative actions.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudentProfile(models.Model):
    """
    Extended user profile for students.

    Linked to Django's User model via OneToOneField.
    Stores student-specific data such as student ID,
    year group, role, and eligibility status.
    """

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('observer', 'Observer'),
    ]

    YEAR_GROUP_CHOICES = [
        ('year_7', 'Year 7'),
        ('year_8', 'Year 8'),
        ('year_9', 'Year 9'),
        ('year_10', 'Year 10'),
        ('year_11', 'Year 11'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text='Unique student identification number'
    )
    year_group = models.CharField(
        max_length=10,
        choices=YEAR_GROUP_CHOICES,
        default='year_7'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )
    is_eligible = models.BooleanField(
        default=True,
        help_text='Whether the student is eligible to vote'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return (
            f"{self.user.get_full_name()} "
            f"({self.student_id or 'No ID'})"
        )

    @property
    def is_admin(self):
        """Check if the user has admin privileges."""
        return self.role == 'admin'

    @property
    def is_observer(self):
        """Check if the user has observer privileges."""
        return self.role == 'observer'

    @property
    def is_student(self):
        """Check if the user is a regular student."""
        return self.role == 'student'


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create or update
    a StudentProfile when a User is created or saved.
    """
    if created:
        StudentProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class AuditLog(models.Model):
    """
    Tracks all administrative actions for accountability.

    Records who performed an action, what they did,
    which record was affected, and when it happened.
    """

    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('publish', 'Published'),
        ('close', 'Closed'),
        ('export', 'Exported'),
        ('eligibility', 'Changed Eligibility'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    target_model = models.CharField(
        max_length=50,
        blank=True,
        help_text='The model type that was affected'
    )
    target_id = models.IntegerField(
        null=True,
        blank=True,
        help_text='The ID of the affected record'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return (
            f"{self.user} — {self.get_action_display()} — "
            f"{self.description[:50]}"
        )