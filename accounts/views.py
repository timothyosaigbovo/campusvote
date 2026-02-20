"""
Views for the accounts app.

Handles user registration, authentication, profile management,
and password reset flows with appropriate feedback messages.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ProfileUpdateForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)


def register_view(request):
    """
    Handle new user registration.
    Creates both User and StudentProfile records.
    Redirects authenticated users to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('elections:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Welcome to CampusVote, {user.first_name}! '
                f'Your account has been created successfully.'
            )
            return redirect('elections:dashboard')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login with appropriate error feedback.
    Redirects authenticated users to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('elections:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                f'Welcome back, {user.first_name}!'
            )
            # Redirect to 'next' parameter if present
            next_url = request.GET.get('next', 'elections:dashboard')
            return redirect(next_url)
        else:
            messages.error(
                request,
                'Invalid username or password. Please try again.'
            )
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout with confirmation message.
    Only accepts POST requests for CSRF protection.
    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('elections:home')
    return redirect('elections:dashboard')


@login_required
def profile_view(request):
    """Display the current user's profile information."""
    return render(request, 'accounts/profile.html', {
        'profile': request.user.profile,
    })


@login_required
def profile_edit_view(request):
    """
    Handle profile updates with immediate feedback.
    Allows users to edit their name, email, year group,
    and profile image.
    """
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('accounts:profile')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request, 'accounts/profile_edit.html', {'form': form}
    )


class CustomPasswordResetView(PasswordResetView):
    """Password reset with custom template and form."""
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Confirmation that password reset email was sent."""
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Enter new password after following reset link."""
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete confirmation."""
    template_name = 'accounts/password_reset_complete.html'