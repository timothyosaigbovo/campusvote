#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser if none exists
python manage.py create_superuser_if_none
```

Press **Ctrl+S**.

---

### Step 3: Add environment variables on Render

Go to Render dashboard → **Environment** → click **"Edit"** → add these 3:

| Key | Value |
|-----|-------|
| `DJANGO_SU_NAME` | `admin` |
| `DJANGO_SU_EMAIL` | `admin@campusvote.com` |
| `DJANGO_SU_PASSWORD` | Choose a strong password (e.g. `CampusVote2026!`) |