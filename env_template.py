"""
Environment variables for local development.
This file must NEVER be committed to version control.
Copy this file as env.py and update with your values.
"""

import os

# Django secret key — generate a new one for production
os.environ.setdefault(
    'SECRET_KEY',
    'your-secret-key-change-this-in-production'
)

# Set to 'True' for local development only
os.environ.setdefault('DEBUG', 'True')

# Database URL — PostgreSQL recommended for production
os.environ.setdefault(
    'DATABASE_URL',
    'sqlite:///db.sqlite3'
)

# Allowed hosts
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1')

# Email settings (console backend used by default in development)
os.environ.setdefault(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'
)