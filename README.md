# CampusVote — Student Election Management System

![CampusVote](docs/responsive-mockup.png)

**CampusVote** is a full-stack Django web application that enables schools and colleges to manage student elections digitally. It provides a secure, transparent, and accessible platform for creating elections, managing candidates, casting votes, and publishing results.

**Live Site:** [CampusVote on Render](https://campusvote-smpp.onrender.com)

**Repository:** [GitHub — CampusVote](https://github.com/timothyosaigbovo/campusvote)

---

## Table of Contents

- [Project Overview](#project-overview)
- [User Experience (UX)](#user-experience-ux)
- [User Stories](#user-stories)
- [Features](#features)
- [Data Schema](#data-schema)
- [CRUD Operations](#crud-operations)
- [Security Features](#security-features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

---

## Project Overview

### Rationale

Student elections are a fundamental part of school and college governance. Many institutions still rely on paper ballots, which are time-consuming to count, difficult to audit, and prone to disputes over fairness. CampusVote addresses this by providing a digital solution that is secure, transparent, and easy to use.

### Target Audience

CampusVote serves three distinct user groups:

- **Students (Voters):** Year 7–11 students who need a simple, accessible way to view candidates, cast their votes, and check results.
- **Administrators (Election Committee):** Staff or senior students who create and manage elections, positions, candidates, and voter eligibility.
- **Observers:** Staff members or student representatives who need read-only access to published results and turnout statistics for independent verification.

### Value Proposition

CampusVote provides value to its users by:

- **Eliminating paper ballots** — reducing waste, counting errors, and administrative burden.
- **Enforcing election integrity** — database-level constraints prevent duplicate voting, ensuring one vote per student per position.
- **Providing transparency** — a full audit log records every administrative action, supporting fair dispute resolution.
- **Delivering real-time analytics** — turnout statistics and visual charts give administrators immediate insight into participation.
- **Being accessible** — responsive design ensures students can vote from any device, including mobile phones.

---

## User Experience (UX)

### Strategy Plane

**Project Goal:** Build a secure, database-backed election management system for schools and colleges that handles the full election lifecycle — from creation through to result publication.

**Business Goals:**
- Modernise the student election process in educational institutions.
- Ensure election integrity through technical safeguards rather than manual oversight.
- Provide audit trails for accountability and transparency.

**User Goals:**
- Students want a quick, intuitive voting experience with clear confirmation.
- Admins want full control over the election lifecycle with minimal friction.
- Observers want trustworthy, independently verifiable result data.

### Scope Plane

**Feature Planning:**

1. **Must Have (MVP):** User authentication, election CRUD, position and candidate management, voting with duplicate prevention, results display, role-based access control.
2. **Should Have:** Audit logging, analytics with charts, CSV export, voter eligibility management, password reset, progress indicators.
3. **Could Have (Future):** Email notifications on election start/end, candidate self-nomination workflow, real-time WebSocket vote count updates, multi-language support.

All "Must Have" and "Should Have" features have been fully implemented.

### Structure Plane

The application is structured around three Django apps, each with a clear responsibility:

| App | Purpose | Primary Users |
|-----|---------|---------------|
| `accounts` | Authentication, registration, profile management, password reset | All users |
| `elections` | Election browsing, voting, results viewing | Students, Observers |
| `management` | CRUD operations, analytics, audit logs, voter management | Admins, Observers |

### Skeleton Plane

**Wireframes:**

Wireframes were created for mobile, tablet, and desktop viewports using Balsamiq. They are stored in the `docs/wireframes/` directory.

| Page | Mobile | Tablet | Desktop |
|------|--------|--------|---------|
| Home | [View](docs/wireframes/home-mobile.png) | [View](docs/wireframes/home-tablet.png) | [View](docs/wireframes/home-desktop.png) |
| Dashboard | [View](docs/wireframes/dashboard-mobile.png) | [View](docs/wireframes/dashboard-tablet.png) | [View](docs/wireframes/dashboard-desktop.png) |
| Election Detail | [View](docs/wireframes/election-detail-mobile.png) | [View](docs/wireframes/election-detail-tablet.png) | [View](docs/wireframes/election-detail-desktop.png) |
| Voting Page | [View](docs/wireframes/cast-vote-mobile.png) | [View](docs/wireframes/cast-vote-tablet.png) | [View](docs/wireframes/cast-vote-desktop.png) |
| Results | [View](docs/wireframes/results-mobile.png) | [View](docs/wireframes/results-tablet.png) | [View](docs/wireframes/results-desktop.png) |
| Admin Dashboard | [View](docs/wireframes/admin-dashboard-mobile.png) | [View](docs/wireframes/admin-dashboard-tablet.png) | [View](docs/wireframes/admin-dashboard-desktop.png) |

### Surface Plane

- **Colour Scheme:** Bootstrap 5 blue (`#0d6efd`) as primary colour for trust and authority. Hero section gradient from `#0d6efd` to `#084298`. Status colours follow conventions: green for active, amber for warning, red for closed.
- **Typography:** System font stack for fast rendering and native feel across platforms.
- **Layout:** Consistent card-based layout with Bootstrap 5 grid for responsiveness.
- **Iconography:** Bootstrap Icons paired with text labels for accessibility.
- **Feedback:** Dismissible Bootstrap alerts with colour coding and auto-dismiss after 5 seconds.
- **Accessibility:** Skip-to-content link, focus indicators, semantic HTML, ARIA labels, WCAG AA colour contrast, no autoplay media.

---

## User Stories

### Student (Voter) Stories

| # | User Story | Implemented |
|---|-----------|:-----------:|
| 1 | As a student, I want to log in using secure authentication, so that only verified and eligible users can access the voting system. | ✅ |
| 2 | As a student, I want to reset my password via a secure token link sent to my email, so that I can regain access safely. | ✅ |
| 3 | As a student, I want my session to expire after inactivity, so that my account remains secure on shared devices. | ✅ |
| 4 | As a student, I want clear error messages if login fails, so that I understand what action to take. | ✅ |
| 5 | As a student, I want to see categorised active, upcoming, and closed elections on my dashboard. | ✅ |
| 6 | As a student, I want to view election details including timeline, eligibility, and candidates. | ✅ |
| 7 | As a student, I want the interface to be responsive, so I can vote on any device. | ✅ |
| 8 | As a student, I want to view positions in a structured layout to complete voting logically. | ✅ |
| 9 | As a student, I want to view candidate profiles with photo, manifesto, and details. | ✅ |
| 10 | As a student, I want to cast one vote per position with election integrity maintained. | ✅ |
| 11 | As a student, I want duplicate voting prevented through database validation. | ✅ |
| 12 | As a student, I want immediate confirmation when my vote is recorded. | ✅ |
| 13 | As a student, I want a progress indicator showing which positions I have voted on. | ✅ |
| 14 | As a student, I want graceful error handling if something goes wrong. | ✅ |
| 15 | As a student, I want to view results only after they are officially published. | ✅ |
| 16 | As a student, I want results with vote counts and percentage breakdowns. | ✅ |
| 17 | As a student, I want visual charts to interpret results easily. | ✅ |

### Admin / Election Committee Stories

| # | User Story | Implemented |
|---|-----------|:-----------:|
| 1 | As an admin, I want to create, edit, activate, and close elections. | ✅ |
| 2 | As an admin, I want to define start/end times with enforcement. | ✅ |
| 3 | As an admin, I want to archive past elections. | ✅ |
| 4 | As an admin, I want full CRUD for positions within elections. | ✅ |
| 5 | As an admin, I want to manage candidates with images and manifestos. | ✅ |
| 6 | As an admin, I want form validation on candidate data. | ✅ |
| 7 | As an admin, I want to manage voter eligibility. | ✅ |
| 8 | As an admin, I want role-based access control (Admin, Student, Observer). | ✅ |
| 9 | As an admin, I want to suspend voters if misconduct is detected. | ✅ |
| 10 | As an admin, I want real-time vote counts. | ✅ |
| 11 | As an admin, I want graphical analytics (bar and doughnut charts). | ✅ |
| 12 | As an admin, I want voter turnout statistics by year group. | ✅ |
| 13 | As an admin, I want to export results to CSV. | ✅ |
| 14 | As an admin, I want the system to log all administrative actions. | ✅ |
| 15 | As an admin, I want to review audit logs for dispute resolution. | ✅ |

### Observer Stories

| # | User Story | Implemented |
|---|-----------|:-----------:|
| 1 | As an observer, I want read-only access to published results. | ✅ |
| 2 | As an observer, I want to see turnout summaries for verification. | ✅ |

---

## Features

### Public Pages

- **Home Page:** Hero section with platform description, active/upcoming elections, and register/login CTAs.
- **Custom 404 Page:** User-friendly error page with navigation back to home.
- **Custom 500 Page:** Graceful server error page.

### Student Features

- **Registration:** Account creation with unique student ID, email, year group, and password validation.
- **Login / Logout:** Django authentication with custom Bootstrap templates.
- **Password Reset:** Full four-step token-based reset flow.
- **Profile View / Edit:** View and update personal information.
- **Dashboard:** Elections categorised by status with voting progress bars.
- **Election Detail:** Positions with candidates and voting status per position.
- **Candidate Detail:** Full profile with photo, manifesto, and student details.
- **Voting:** Radio-button candidate selection with confirmation prompt. Database `UniqueConstraint` prevents duplicate votes.
- **Results:** Vote counts, percentages, and Chart.js doughnut charts (only when published).

### Admin Features

- **Management Dashboard:** Stats overview with quick-action buttons and recent activity feed.
- **Election CRUD:** Full lifecycle management with date validation and results publishing.
- **Position CRUD:** Add/edit/delete positions with display ordering.
- **Candidate CRUD:** Student selection, manifesto, photo upload (max 5 MB), approval toggle.
- **Voter Management:** Toggle eligibility to suspend/reinstate voting rights.
- **Analytics:** Turnout by year group with progress bars, vote distribution with Chart.js charts.
- **CSV Export:** Download results with UTF-8 BOM for Excel compatibility.
- **Audit Logs:** Filterable log of all admin actions with timestamp, user, action type, and IP address.

---

## Data Schema

### Entity Relationship Diagram

![Database Schema](docs/erd.png)

### Models

**StudentProfile** (One-to-One → User)

| Field | Type | Purpose |
|-------|------|---------|
| `user` | OneToOneField(User) | Links to Django User model |
| `student_id` | CharField (unique) | Institutional student ID |
| `year_group` | CharField (choices) | Year 7, 8, 9, 10, or 11 |
| `role` | CharField (choices) | student, admin, or observer |
| `is_eligible` | BooleanField | Whether the student may vote |
| `profile_image` | ImageField | Optional profile photo |

**Election**

| Field | Type | Purpose |
|-------|------|---------|
| `title` | CharField | Election name |
| `description` | TextField | Rules and guidelines |
| `start_date` / `end_date` | DateTimeField | Voting window |
| `status` | CharField | draft, active, closed, archived |
| `results_published` | BooleanField | Whether results are visible |
| `eligible_year_groups` | CharField | Comma-separated year groups |

**Position** (FK → Election) — title, description, display_order, max_candidates

**Candidate** (FK → Position, FK → StudentProfile) — manifesto, photo, is_approved. `UniqueConstraint(student_profile, position)`.

**Vote** (FK → StudentProfile, Position, Candidate) — cast_at. `UniqueConstraint(student_profile, position)` — **one vote per student per position at database level**.

**AuditLog** (FK → User) — action, description, target_model, target_id, ip_address, timestamp.

### Relationships Summary

```
User ──── 1:1 ──── StudentProfile
                        │
                 ┌──────┼──────┐
            Candidate  Vote  AuditLog
                 │      │
                 └──┬───┘
                 Position
                    │
                 Election
```

---

## CRUD Operations

### Elections

| Operation | URL | Method | Access |
|-----------|-----|--------|--------|
| **Create** | `/management/elections/create/` | POST | Admin |
| **Read** | `/management/elections/<id>/` | GET | Admin |
| **Update** | `/management/elections/<id>/edit/` | POST | Admin |
| **Delete** | `/management/elections/<id>/delete/` | POST | Admin |

### Positions

| Operation | URL | Method | Access |
|-----------|-----|--------|--------|
| **Create** | `/management/elections/<id>/positions/create/` | POST | Admin |
| **Update** | `/management/positions/<id>/edit/` | POST | Admin |
| **Delete** | `/management/positions/<id>/delete/` | POST | Admin |

### Candidates

| Operation | URL | Method | Access |
|-----------|-----|--------|--------|
| **Create** | `/management/positions/<id>/candidates/create/` | POST | Admin |
| **Read** | `/elections/candidate/<id>/` | GET | Authenticated |
| **Update** | `/management/candidates/<id>/edit/` | POST | Admin |
| **Delete** | `/management/candidates/<id>/delete/` | POST | Admin |

### Votes (Create-only — immutable by design)

| Operation | URL | Method | Access |
|-----------|-----|--------|--------|
| **Create** | `/elections/vote/<position_id>/` | POST | Eligible students |
| **Read** | `/elections/results/<id>/` | GET | All (when published) |

---

## Security Features

- **Authentication:** Django PBKDF2 password hashing, session timeout (30 min), token-based password reset.
- **Secrets:** `SECRET_KEY` and `DATABASE_URL` stored as environment variables, `env.py` in `.gitignore`.
- **Production headers:** `SECURE_SSL_REDIRECT`, HSTS, secure cookies, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF`.
- **Role-based access:** `@admin_required` and `@admin_or_observer_required` decorators on views, template-level conditional rendering.
- **Three-layer validation:** Form-level (Django forms), Model-level (`clean()` methods), Database-level (`UniqueConstraint`).
- **CSRF protection:** All forms include `{% csrf_token %}`, all state changes use POST.

---

## Technologies Used

### Languages

- **Python 3.12** — Django framework
- **HTML5** — Semantic structure
- **CSS3** — Custom styling
- **JavaScript (ES6)** — Client-side interactions

### Frameworks & Libraries

- **[Django 4.2 LTS](https://www.djangoproject.com/)** — Web framework
- **[Bootstrap 5.3](https://getbootstrap.com/)** — Responsive CSS framework
- **[Bootstrap Icons](https://icons.getbootstrap.com/)** — Icon library
- **[Chart.js](https://www.chartjs.org/)** — Results visualisation
- **[WhiteNoise](https://whitenoise.readthedocs.io/)** — Static file serving
- **[dj-database-url](https://pypi.org/project/dj-database-url/)** — Database configuration
- **[Pillow](https://pillow.readthedocs.io/)** — Image processing
- **[Gunicorn](https://gunicorn.org/)** — WSGI server
- **[psycopg2-binary](https://pypi.org/project/psycopg2-binary/)** — PostgreSQL adapter

### Database

- **PostgreSQL** — Production (Render)
- **SQLite** — Development

### Tools

- Git, GitHub, Render, Balsamiq, Chrome DevTools, W3C Validators, JSHint, pycodestyle

---

## Testing

**[View Full Testing Documentation → TESTING.md](TESTING.md)**

Covers: manual testing mapped to user stories, CRUD testing, form validation, security testing, duplicate vote prevention, responsiveness, browser compatibility, code validation (HTML/CSS/JS/Python), and Lighthouse auditing.

---

## Deployment

### Render Deployment

1. **Create PostgreSQL database** on Render (Free tier, Frankfurt region).
2. **Create Web Service** connected to GitHub repo:
   - Build Command: `sh build.sh`
   - Start Command: `gunicorn campusvote.wsgi`
3. **Set environment variables:**

   | Variable | Value |
   |----------|-------|
   | `SECRET_KEY` | Django-generated secret key |
   | `DATABASE_URL` | Internal Database URL |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.onrender.com,localhost` |
   | `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` |
   | `PYTHON_VERSION` | `3.12.10` |

4. Click **Create Web Service** — auto-deploys on every `git push`.

### Key Files

| File | Purpose |
|------|---------|
| `Procfile` | Gunicorn start command |
| `build.sh` | Install deps, collectstatic, migrate |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version |

### Local Development

```bash
git clone https://github.com/timothyosaigbovo/campusvote.git
cd campusvote
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp env_template.py env.py     # Edit with your SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Credits

### Code

- [Django documentation](https://docs.djangoproject.com/) — authentication, forms, model validation, deployment.
- [Bootstrap 5 documentation](https://getbootstrap.com/docs/5.3/) — layout, components, utilities.
- [Chart.js documentation](https://www.chartjs.org/docs/) — doughnut and bar charts.
- [WhiteNoise](https://whitenoise.readthedocs.io/) — static file configuration.
- [dj-database-url](https://pypi.org/project/dj-database-url/) — database URL parsing.

All application logic, templates, and custom CSS/JavaScript are original work.

### Media

- **Bootstrap Icons** — [icons.getbootstrap.com](https://icons.getbootstrap.com/) — MIT licence.

### Acknowledgements

- Gateway Qualifications for the Level 5 Diploma in Web Application Development assessment criteria.
- The Django community for comprehensive documentation and tutorials.
- Bootstrap team for the responsive CSS framework.

---

*This project was created as part of the Level 5 Diploma in Web Application Development — Unit 3: Back End Development.*
