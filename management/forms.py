"""
Forms for the management app.

Provides admin forms for creating and editing elections,
positions, candidates, and managing voter eligibility.
All forms include comprehensive validation.
"""

from django import forms
from django.core.exceptions import ValidationError
from elections.models import Election, Position, Candidate
from accounts.models import StudentProfile


class ElectionForm(forms.ModelForm):
    """
    Form for creating and editing elections.
    Includes date validation and year group selection.
    """

    class Meta:
        model = Election
        fields = [
            'title', 'description', 'start_date', 'end_date',
            'status', 'eligible_year_groups',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Election title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Election description and rules',
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'eligible_year_groups': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':
                    'year_7,year_8,year_9,year_10,year_11',
            }),
        }

    def clean(self):
        """Validate date range and status transitions."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError(
                    'End date must be after start date.'
                )
        return cleaned_data


class PositionForm(forms.ModelForm):
    """Form for creating and editing positions."""

    class Meta:
        model = Position
        fields = [
            'title', 'description', 'display_order',
            'max_candidates',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':
                    'Position title (e.g., Head Boy)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder':
                    'Role description and responsibilities',
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'max_candidates': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
            }),
        }


class CandidateForm(forms.ModelForm):
    """
    Form for creating and editing candidate records.
    Includes validation for image type and manifesto length.
    """

    class Meta:
        model = Candidate
        fields = [
            'student_profile', 'manifesto', 'photo',
            'is_approved',
        ]
        widgets = {
            'student_profile': forms.Select(attrs={
                'class': 'form-select',
            }),
            'manifesto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder':
                    'Campaign manifesto (max 2000 characters)',
                'maxlength': 2000,
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, position=None, **kwargs):
        super().__init__(*args, **kwargs)
        if position:
            # Only show students not already candidates
            existing_candidate_profiles = (
                Candidate.objects.filter(
                    position=position
                ).exclude(
                    pk=self.instance.pk
                    if self.instance.pk else None
                ).values_list(
                    'student_profile_id', flat=True
                )
            )

            self.fields['student_profile'].queryset = (
                StudentProfile.objects.filter(
                    role='student'
                ).exclude(
                    pk__in=existing_candidate_profiles
                )
            )

    def clean_photo(self):
        """Validate uploaded image file type and size."""
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'content_type'):
            allowed_types = [
                'image/jpeg', 'image/png', 'image/webp'
            ]
            if photo.content_type not in allowed_types:
                raise ValidationError(
                    'Only JPEG, PNG, and WebP images '
                    'are accepted.'
                )
            # Limit file size to 5MB
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError(
                    'Image file size must be less than 5MB.'
                )
        return photo


class VoterEligibilityForm(forms.ModelForm):
    """Form for managing voter eligibility status."""

    class Meta:
        model = StudentProfile
        fields = ['is_eligible']
        widgets = {
            'is_eligible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }