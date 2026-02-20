"""
Models for the elections app.

Defines the Election, Position, Candidate, and Vote models
with comprehensive validation and database-level constraints
to ensure data integrity.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import StudentProfile


class Election(models.Model):
    """
    Represents a student election event.

    Contains metadata about the election including dates,
    status, and eligible year groups. Status transitions
    control the election lifecycle.
    """

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    eligible_year_groups = models.CharField(
        max_length=100,
        default='year_7,year_8,year_9,year_10,year_11',
        help_text='Comma-separated year groups '
                  '(e.g., year_7,year_8,year_9)'
    )
    results_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def clean(self):
        """Validate that end date is after start date."""
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError(
                    'End date must be after start date.'
                )

    @property
    def is_active(self):
        """Check if the election is currently active."""
        return self.status == 'active'

    @property
    def is_closed(self):
        """Check if the election has ended."""
        return self.status in ('closed', 'archived')

    @property
    def is_upcoming(self):
        """Check if the election hasn't started yet."""
        return (
            self.status == 'active'
            and self.start_date > timezone.now()
        )

    @property
    def is_in_progress(self):
        """Check if voting is currently open."""
        now = timezone.now()
        return (
            self.status == 'active'
            and self.start_date <= now <= self.end_date
        )

    def get_eligible_year_groups_list(self):
        """Return eligible year groups as a list."""
        return [
            yg.strip()
            for yg in self.eligible_year_groups.split(',')
            if yg.strip()
        ]

    def is_student_eligible(self, student_profile):
        """Check if a specific student can vote."""
        if not student_profile.is_eligible:
            return False
        return (
            student_profile.year_group
            in self.get_eligible_year_groups_list()
        )


class Position(models.Model):
    """
    Represents a position within an election.

    Each election can have multiple positions (e.g.,
    Head Boy, Head Girl, Sports Captain). Candidates
    are assigned to specific positions.
    """

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(
        default=0,
        help_text='Order in which positions are displayed'
    )
    max_candidates = models.IntegerField(
        default=10,
        help_text='Maximum number of candidates allowed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.title} — {self.election.title}"

    def get_vote_counts(self):
        """Return vote counts for each candidate."""
        candidates = self.candidates.filter(is_approved=True)
        return [
            {
                'candidate': c,
                'votes': Vote.objects.filter(
                    position=self, candidate=c
                ).count(),
            }
            for c in candidates
        ]

    def total_votes(self):
        """Return the total number of votes for this position."""
        return Vote.objects.filter(position=self).count()


class Candidate(models.Model):
    """
    Represents a student standing for a position.

    Links a StudentProfile to a Position with additional
    campaign information such as manifesto and photo.
    """

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    student_profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='candidacies'
    )
    manifesto = models.TextField(
        max_length=2000,
        blank=True,
        help_text='Campaign manifesto (max 2000 characters)'
    )
    photo = models.ImageField(
        upload_to='candidates/',
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(
        default=True,
        help_text='Whether the candidacy has been approved'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['student_profile__user__last_name']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        constraints = [
            models.UniqueConstraint(
                fields=['position', 'student_profile'],
                name='unique_candidate_per_position'
            )
        ]

    def __str__(self):
        return (
            f"{self.student_profile.user.get_full_name()} "
            f"— {self.position.title}"
        )

    def vote_count(self):
        """Return the number of votes this candidate received."""
        return Vote.objects.filter(
            position=self.position,
            candidate=self
        ).count()


class Vote(models.Model):
    """
    Records a single vote cast by a student.

    Each student can vote once per position, enforced
    at the database level via UniqueConstraint.
    The candidate chosen is recorded along with a timestamp.
    """

    student_profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes_received'
    )
    cast_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-cast_at']
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        constraints = [
            models.UniqueConstraint(
                fields=['student_profile', 'position'],
                name='one_vote_per_student_per_position'
            )
        ]

    def __str__(self):
        return (
            f"{self.student_profile} voted for "
            f"{self.candidate} — {self.position.title}"
        )

    def clean(self):
        """Validate the vote before saving."""
        # Check election is active
        if not self.position.election.is_in_progress:
            raise ValidationError(
                'Voting is not currently open for this election.'
            )
        # Check student eligibility
        if not self.position.election.is_student_eligible(
            self.student_profile
        ):
            raise ValidationError(
                'You are not eligible to vote in this election.'
            )
        # Check candidate is approved
        if not self.candidate.is_approved:
            raise ValidationError(
                'This candidate has not been approved.'
            )