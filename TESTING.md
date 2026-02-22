# CampusVote — Testing Documentation

This document provides a comprehensive record of all testing performed on the CampusVote application, including manual testing mapped to user stories, CRUD operation testing, validation testing, security testing, responsiveness testing, browser compatibility, code validation, and Lighthouse auditing.

---

## Table of Contents

- [Manual Testing — User Story Testing](#manual-testing--user-story-testing)
- [CRUD Operation Testing](#crud-operation-testing)
- [Form Validation Testing](#form-validation-testing)
- [Security & Access Control Testing](#security--access-control-testing)
- [Duplicate Vote Prevention Testing](#duplicate-vote-prevention-testing)
- [Responsiveness Testing](#responsiveness-testing)
- [Browser Compatibility Testing](#browser-compatibility-testing)
- [Code Validation](#code-validation)
- [Lighthouse Testing](#lighthouse-testing)
- [Bugs Found and Fixes](#bugs-found-and-fixes)
- [Known Issues](#known-issues)

---

## Manual Testing — User Story Testing

Each user story from the project planning phase was tested manually. Results are documented below with the test procedure, expected result, actual result, and pass/fail status.

### Student Authentication Stories

| # | User Story | Test Procedure | Expected Result | Actual Result | Pass/Fail |
|---|-----------|----------------|-----------------|---------------|:---------:|
| S1 | Log in with secure authentication | Navigate to `/accounts/login/`. Enter valid username and password. Click "Login". | User is redirected to dashboard. Welcome message displayed. | User redirected to dashboard. "Welcome back, [name]!" success message displayed. | ✅ Pass |
| S2 | Password reset via email token | Click "Forgot Password" on login page. Enter registered email. Check email for token link. Click link. Enter new password. | Password is changed. User can log in with new password. | Email sent (console backend in development). Token link opens password reset form. Password changed successfully. Login works with new password. | ✅ Pass |
| S3 | Session expires after inactivity | Log in. Wait 30+ minutes without activity. Attempt to access a protected page. | User is redirected to login page. | User redirected to login page with "Please log in to continue" message. | ✅ Pass |
| S4 | Clear error messages on login failure | Enter incorrect username or password. Click "Login". | Error message displayed explaining the issue. | "Invalid username or password. Please try again." error displayed. | ✅ Pass |

### Student Election & Voting Stories

| # | User Story | Test Procedure | Expected Result | Actual Result | Pass/Fail |
|---|-----------|----------------|-----------------|---------------|:---------:|
| S5 | See categorised elections | Log in as student. Navigate to dashboard. | Elections grouped into Active, Upcoming, and Closed sections. | Elections displayed in three clearly labelled sections with appropriate status badges. | ✅ Pass |
| S6 | View election details | Click on an election from the dashboard. | Election detail page shows title, dates, positions, and candidates. | All election information displayed correctly. Positions listed in display order. | ✅ Pass |
| S7 | Responsive interface | Access the application on mobile, tablet, and desktop viewports. | Layout adapts to screen size. All functionality accessible. | Bootstrap grid collapses correctly. Cards stack on mobile. Navigation becomes hamburger menu. | ✅ Pass |
| S8 | View positions in structured layout | Navigate to election detail for an active election. | Positions displayed in order with clear labels and candidate counts. | Positions displayed in `display_order`, each with title, description, candidate count, and voting status. | ✅ Pass |
| S9 | View candidate profiles | Click on a candidate name from the election detail page. | Candidate detail page shows photo, manifesto, student ID, and year group. | Full candidate profile displayed with all fields. Photo displayed if uploaded, initials placeholder if not. | ✅ Pass |
| S10 | Cast one vote per position | Navigate to voting page. Select a candidate. Click "Cast Vote". Confirm. | Vote recorded. Success message displayed. | Vote recorded. "Your vote for [Position] has been recorded!" success message. Redirect to election detail. | ✅ Pass |
| S11 | Prevent duplicate voting | Attempt to vote for the same position twice by navigating directly to the vote URL. | Error message displayed. Duplicate vote prevented. | "You have already voted for this position" error. Database `IntegrityError` caught gracefully. | ✅ Pass |
| S12 | Immediate visual confirmation | Cast a vote. | Success message appears immediately. | Green success alert appears, auto-dismisses after 5 seconds. | ✅ Pass |
| S13 | Progress indicator | Vote for some positions in an election, not all. Return to dashboard. | Progress bar shows percentage of positions voted on. | Progress bar shows "2 of 4 positions voted" with 50% fill. | ✅ Pass |
| S14 | Graceful error handling | Attempt to vote in a closed election by manipulating the URL. | Error message displayed. Vote not recorded. | "Voting is not currently open for this election" error. User redirected. | ✅ Pass |
| S15 | Results only when published | Try to access results for an unpublished election. | Results not shown. | "Results have not been published yet" message displayed. | ✅ Pass |
| S16 | Numeric counts and percentages | View published results. | Each candidate shows vote count and percentage. | Vote counts and percentages displayed correctly, summing to 100% per position. | ✅ Pass |
| S17 | Visual charts | View published results. | Chart.js charts displayed for each position. | Doughnut charts rendered with colour-coded segments. | ✅ Pass |

### Admin Stories

| # | User Story | Test Procedure | Expected Result | Actual Result | Pass/Fail |
|---|-----------|----------------|-----------------|---------------|:---------:|
| A1 | Create, edit, activate, close elections | Create election. Edit title. Change status. | All operations succeed. | Election created, updated, status changed. Audit log entries created. | ✅ Pass |
| A2 | Define start/end times with enforcement | Create election with end date before start date. | Validation error. | "End date must be after start date" error displayed. Election not saved. | ✅ Pass |
| A3 | Archive past elections | Change closed election status to "archived". | Election archived. | Status updated. | ✅ Pass |
| A4 | CRUD positions | Create, edit, delete a position. | All operations succeed. | Position created, updated, deleted. Each shows success message. | ✅ Pass |
| A5 | CRUD candidates with images | Create candidate with photo and manifesto. Edit. Delete. | All operations succeed. Photo uploaded. | Candidate created with photo. Edit updates manifesto. Delete cascades to votes. | ✅ Pass |
| A6 | Candidate form validation | Upload non-image file. Exceed manifesto limit. Leave required fields blank. | Validation errors for each case. | Appropriate errors displayed for invalid file, long manifesto, blank fields. | ✅ Pass |
| A7 | Manage eligible voters | Navigate to voter management. | Voter list displayed with eligibility status. | All student profiles shown with eligibility toggle. | ✅ Pass |
| A8 | Role-based access control | Student attempts `/management/`. Admin accesses `/management/`. | Student denied. Admin granted. | Student redirected with permission error. Admin accesses dashboard. | ✅ Pass |
| A9 | Suspend voter | Toggle eligibility. Have student attempt to vote. | Student cannot vote when ineligible. | Eligibility toggled. Ineligible student sees error when attempting to vote. | ✅ Pass |
| A10 | Real-time vote counts | Access analytics for election with votes. | Vote counts displayed per candidate. | Counts, percentages, and winner indicators displayed correctly. | ✅ Pass |
| A11 | Graphical analytics | Access analytics page. | Charts displayed. | Chart.js bar charts rendered correctly. | ✅ Pass |
| A12 | Turnout by year group | View analytics with voters from multiple year groups. | Turnout broken down by year group. | Year group breakdown with eligible/voted counts and percentages. Progress bars. | ✅ Pass |
| A13 | CSV export | Click "Export CSV". | CSV file downloaded. | CSV downloaded with columns: Position, Candidate, Year Group, Votes, Percentage. Audit log entry created. | ✅ Pass |
| A14 | System logs admin actions | Perform admin actions. Check audit logs. | Each action recorded. | All actions logged with timestamp, user, action type, description, and IP address. | ✅ Pass |
| A15 | Review audit logs | Navigate to audit log page. Filter by action type. | Filtered entries displayed. | Audit log list filterable by action type. Most recent first. | ✅ Pass |

### Observer Stories

| # | User Story | Test Procedure | Expected Result | Actual Result | Pass/Fail |
|---|-----------|----------------|-----------------|---------------|:---------:|
| O1 | Read-only access to results | Log in as observer. View analytics. Attempt election edit. | Analytics visible. Edit denied. | Observer views analytics. Edit redirects with permission error. | ✅ Pass |
| O2 | Turnout summaries | Log in as observer. Access analytics. | Turnout data visible. | Overall turnout and year group breakdown displayed. | ✅ Pass |

---

## CRUD Operation Testing

### Election CRUD

| Operation | Action | Expected | Actual | Pass/Fail |
|-----------|--------|----------|--------|:---------:|
| Create | Filled form with valid data | Election appears in list | Created. "Election created successfully!" | ✅ Pass |
| Read | Clicked election title | Detail page loads | All info displayed correctly | ✅ Pass |
| Update | Edited title and description | Changes saved | Updated. "Election updated successfully!" | ✅ Pass |
| Delete | Clicked Delete, confirmed | Election removed | Deleted. Positions, candidates, and votes cascade deleted. | ✅ Pass |

### Position CRUD

| Operation | Action | Expected | Actual | Pass/Fail |
|-----------|--------|----------|--------|:---------:|
| Create | Added position with title | Position appears | Created. Visible in election detail. | ✅ Pass |
| Update | Changed title | Updated title reflected | Title updated immediately. | ✅ Pass |
| Delete | Deleted position with candidate | Both removed | Position and candidate deleted (cascade). | ✅ Pass |

### Candidate CRUD

| Operation | Action | Expected | Actual | Pass/Fail |
|-----------|--------|----------|--------|:---------:|
| Create | Added candidate with photo | Candidate appears | Created with uploaded photo. | ✅ Pass |
| Read | Clicked candidate name | Detail page loads | Photo, manifesto, details displayed. | ✅ Pass |
| Update | Edited manifesto | Updated text visible | Manifesto updated. | ✅ Pass |
| Delete | Deleted candidate | Candidate removed | Deleted. Associated votes removed. | ✅ Pass |

---

## Form Validation Testing

### Registration Form

| Test | Input | Expected | Actual | Pass/Fail |
|------|-------|----------|--------|:---------:|
| Blank username | Empty field | "This field is required." | Error displayed. | ✅ Pass |
| Duplicate email | Already registered | "A user with this email already exists." | Error displayed. | ✅ Pass |
| Duplicate student ID | Already in use | "This student ID is already registered." | Error displayed. | ✅ Pass |
| Weak password | "password123" | "This password is too common." | Error displayed. | ✅ Pass |
| Password mismatch | Different passwords | "The two password fields didn't match." | Error displayed. | ✅ Pass |
| Valid submission | All fields valid | Account created | Created. Success message. Profile auto-created via signal. | ✅ Pass |

### Election Form

| Test | Input | Expected | Actual | Pass/Fail |
|------|-------|----------|--------|:---------:|
| End before start | End date earlier | "End date must be after start date." | Error displayed. | ✅ Pass |
| Blank title | Empty | "This field is required." | Error displayed. | ✅ Pass |
| Valid submission | All valid | Election created | Created successfully. | ✅ Pass |

### Candidate Form

| Test | Input | Expected | Actual | Pass/Fail |
|------|-------|----------|--------|:---------:|
| Invalid image | `.txt` file | "Please upload a valid image." | Error displayed. | ✅ Pass |
| Oversized image | 10 MB | "Image must be under 5 MB." | Error displayed. | ✅ Pass |
| Manifesto too long | 3000+ characters | max_length validation | Error displayed. | ✅ Pass |
| Valid submission | Valid data | Candidate created | Created. Photo uploaded. | ✅ Pass |

### Vote Form

| Test | Input | Expected | Actual | Pass/Fail |
|------|-------|----------|--------|:---------:|
| No candidate selected | Submit empty | "Please select a candidate." | Error displayed. | ✅ Pass |
| Ineligible student | Wrong year group | "Not eligible to vote." | Error displayed. | ✅ Pass |
| Closed election | Vote URL for closed | "Voting is not open." | Error displayed. | ✅ Pass |
| Valid vote | Select and confirm | Vote recorded | Created. Success message. "Voted" badge shown. | ✅ Pass |

---

## Security & Access Control Testing

### URL Access Testing

| User Role | URL Attempted | Expected | Actual | Pass/Fail |
|-----------|--------------|----------|--------|:---------:|
| Not logged in | `/elections/dashboard/` | Redirect to login | Redirected to `/accounts/login/` | ✅ Pass |
| Student | `/management/` | Access denied | Redirected with permission error | ✅ Pass |
| Student | `/management/elections/create/` | Access denied | Redirected with permission error | ✅ Pass |
| Observer | `/management/elections/1/edit/` | Access denied | Redirected with permission error | ✅ Pass |
| Observer | `/management/elections/1/analytics/` | Allowed | Analytics page displayed | ✅ Pass |
| Admin | All `/management/` URLs | Full access | All pages accessible | ✅ Pass |

### CSRF & Secrets Testing

| Test | Expected | Actual | Pass/Fail |
|------|----------|--------|:---------:|
| POST without CSRF token | 403 Forbidden | 403 Forbidden | ✅ Pass |
| CSRF token in all forms | Hidden input present | Token present in all forms | ✅ Pass |
| No secrets in repository | No hardcoded secrets | `env.py` in `.gitignore`. Settings read from env vars. | ✅ Pass |
| DEBUG=False in production | No debug pages | Custom 404/500 pages shown | ✅ Pass |

---

## Duplicate Vote Prevention Testing

This is a critical business rule — each student may only vote once per position. Testing at three levels:

| Level | Test | Expected | Actual | Pass/Fail |
|-------|------|----------|--------|:---------:|
| **UI** | Vote button hidden after vote | "Voted" badge replaces button | Badge displayed. No vote link available. | ✅ Pass |
| **View** | Direct URL access after voting | Error message. Vote not duplicated. | "Already voted" error. Redirect to election. | ✅ Pass |
| **Database** | Attempt duplicate via Django shell | `IntegrityError` raised | `IntegrityError: unique constraint violated`. Vote not created. | ✅ Pass |

This three-layer defence ensures duplicate voting is impossible regardless of how the request is made.

---

## Responsiveness Testing

Testing performed using Chrome DevTools device emulation.

| Device / Width | Pages Tested | Result | Notes |
|---------------|-------------|--------|-------|
| iPhone SE (375px) | All | ✅ Pass | Cards stack. Navigation collapses to hamburger. |
| iPhone 12 (390px) | All | ✅ Pass | All functionality accessible. |
| iPad (768px) | All | ✅ Pass | Two-column layout. Tables horizontally scrollable. |
| Desktop (1024px) | All | ✅ Pass | Full three-column layout. |
| Desktop (1440px) | All | ✅ Pass | Content centred. No overflow. |

---

## Browser Compatibility Testing

| Browser | Version | OS | Result |
|---------|---------|-----|--------|
| Chrome | 121+ | Windows | ✅ Pass |
| Firefox | 122+ | Windows | ✅ Pass |
| Safari | 17+ | macOS / iOS | ✅ Pass |
| Edge | 121+ | Windows | ✅ Pass |
| Chrome Mobile | 121+ | Android | ✅ Pass |
| Safari Mobile | 17+ | iOS | ✅ Pass |

---

## Code Validation

### HTML Validation

All pages validated via [W3C Markup Validation Service](https://validator.w3.org/) using rendered page source.

| Page | Result |
|------|--------|
| Home (`/`) | ✅ No errors |
| Login (`/accounts/login/`) | ✅ No errors |
| Register (`/accounts/register/`) | ✅ No errors |
| Dashboard (`/elections/dashboard/`) | ✅ No errors |
| Election Detail (`/elections/election/1/`) | ✅ No errors |
| Cast Vote (`/elections/vote/1/`) | ✅ No errors |
| Results (`/elections/results/1/`) | ✅ No errors |
| Profile (`/accounts/profile/`) | ✅ No errors |
| Admin Dashboard (`/management/`) | ✅ No errors |
| Election List (`/management/elections/`) | ✅ No errors |
| Analytics (`/management/elections/1/analytics/`) | ✅ No errors |
| Audit Logs (`/management/audit-logs/`) | ✅ No errors |
| 404 Page | ✅ No errors |

### CSS Validation

| File | Validator | Result |
|------|-----------|--------|
| `static/css/style.css` | [W3C Jigsaw](https://jigsaw.w3.org/css-validator/) | ✅ No errors |

### JavaScript Validation

| File | Validator | Result |
|------|-----------|--------|
| `static/js/script.js` | [JSHint](https://jshint.com/) (ES6, `bootstrap` global) | ✅ No major issues |

### Python Validation

All Python files checked with `pycodestyle --max-line-length=79`:

| File | Result |
|------|--------|
| `accounts/models.py` | ✅ No errors |
| `accounts/views.py` | ✅ No errors |
| `accounts/forms.py` | ✅ No errors |
| `accounts/urls.py` | ✅ No errors |
| `elections/models.py` | ✅ No errors |
| `elections/views.py` | ✅ No errors |
| `elections/urls.py` | ✅ No errors |
| `management/views.py` | ✅ No errors |
| `management/forms.py` | ✅ No errors |
| `management/decorators.py` | ✅ No errors |
| `management/urls.py` | ✅ No errors |
| `campusvote/settings.py` | ✅ No errors |
| `campusvote/urls.py` | ✅ No errors |

---

## Lighthouse Testing

Audits performed using Chrome DevTools on the deployed application.

| Page | Performance | Accessibility | Best Practices | SEO |
|------|:-----------:|:-------------:|:--------------:|:---:|
| Home | 95 | 98 | 100 | 100 |
| Dashboard | 92 | 97 | 100 | 100 |
| Results (with charts) | 88 | 96 | 100 | 100 |
| Analytics | 90 | 96 | 100 | 100 |

*Screenshots of Lighthouse results are stored in `docs/lighthouse/`.*

---

## Bugs Found and Fixes

### Bug 1: Duplicate Vote IntegrityError Not Handled Gracefully

**Description:** Voting for the same position twice via direct URL caused an unhandled `IntegrityError` (500 error).

**Fix:** Added `try/except IntegrityError` in `cast_vote` view to catch the constraint violation and display a user-friendly message.

**Status:** Fixed.

### Bug 2: Session Timeout Not Redirecting

**Description:** Expired sessions caused generic errors instead of login redirects.

**Fix:** Ensured all views use `@login_required` or custom role decorators that check authentication first.

**Status:** Fixed.

### Bug 3: CSV Export Encoding Issue

**Description:** Accented characters in candidate names caused encoding errors in Excel.

**Fix:** Added UTF-8 BOM (`\ufeff`) to CSV response for Excel compatibility.

**Status:** Fixed.

### Bug 4: Chart.js Not Rendering on Empty Data

**Description:** Positions with zero votes rendered empty circles with no feedback.

**Fix:** Added conditional check — if total votes are zero, display "No votes cast yet" instead of an empty chart.

**Status:** Fixed.

### Bug 5: Project URLs Misconfigured

**Description:** `campusvote/urls.py` contained accounts app placeholder instead of project URL configuration, causing the default Django page to show.

**Fix:** Replaced with correct project URLs including all app includes, media serving, and custom error handlers.

**Status:** Fixed.

---

## Known Issues

1. **Date/time input styling:** `DateTimeField` renders differently across browsers (native picker in Chrome, text input in Firefox/Safari). This is standard browser behaviour and does not affect functionality.

2. **Candidate photo aspect ratio:** Unusual aspect ratio photos may appear stretched on candidate cards. A future improvement would be to crop on upload using Pillow.

3. **Email delivery in production:** Password reset emails require SMTP configuration. In development, emails print to the console. Production deployment needs email settings configured.

4. **Free tier cold start:** Render's free tier spins down after inactivity, causing a 30-50 second delay for the first visitor. Subsequent requests load normally.

These issues are cosmetic or configuration-related and do not affect core functionality, security, or data integrity.

---

*This testing documentation was compiled throughout the development process and updated before final submission.*
