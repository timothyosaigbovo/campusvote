"""
Custom decorators for role-based access control.

Enforces that only users with appropriate roles
can access management views.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator that restricts access to admin users only.
    Redirects non-admin users with an appropriate message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to continue.')
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'Profile not found.')
            return redirect('elections:home')
        if not request.user.profile.is_admin:
            messages.error(
                request,
                'Access denied. Admin privileges required.'
            )
            return redirect('elections:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_or_observer_required(view_func):
    """
    Decorator that allows access to admin and observer users.
    Observers have read-only access to results and analytics.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to continue.')
            return redirect('accounts:login')
        if not hasattr(request.user, 'profile'):
            messages.error(request, 'Profile not found.')
            return redirect('elections:home')
        profile = request.user.profile
        if not (profile.is_admin or profile.is_observer):
            messages.error(
                request,
                'Access denied. Insufficient permissions.'
            )
            return redirect('elections:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper