# SKEC implementation tracker

Updated: 14 November 2026. This tracker reports the repository as inspected, not the requested end-state.

| Module | Status | Evidence and remaining work | External dependency |
|---|---|---|---|
| Authentication and sessions | In Progress | Argon2, HTTP-only sessions, CSRF, reset/invitation tokens, idle/absolute expiry and login-attempt throttling exist. Password-history, account deactivation workflow and reset throttling remain. | SMTP for live reset delivery |
| MFA | In Progress | TOTP secret encryption, enforcement for configured privileged roles and one-time recovery codes are implemented. Administrative recovery and tests for every privileged role remain. | `FIELD_ENCRYPTION_KEY` |
| Email/mobile verification and OTP | In Progress | Hashed, expiring, one-use email and SMS verification challenges with cooldown and rate limiting are implemented. SMS uses a generic HTTP adapter and returns unavailable when unconfigured. | SMTP and approved SMS provider |
| RBAC | In Progress | A database-backed role/permission catalogue now governs protected endpoint access, with scope checks retained in handlers. Super Admin, Exam Staff and Accounts Staff records are provisioned by migration. Their required workflows and complete department/resource scope rules are not implemented. | None |
| Student, faculty and admin ERP | In Progress | Limited attendance, results, assignments, timetable, profiles, notices and invoices are present. The full workflows described in the brief are absent. | Requirements decisions and data migration plan |
| Attendance and examination | In Progress | Basic creation and ownership checks exist. Corrections, approvals, audit history views, schedules, question-paper storage and result workflow are absent. | None |
| Assignment files | In Progress | Private storage, type/size allow-list, owner download checks and a fail-closed ClamAV daemon adapter exist. Linkage to submissions, async scanning and quarantine operations remain. | ClamAV service |
| Fees and Razorpay | In Progress | Database-calculated amount, signature checks, webhook dedupe/locking and reconciliation states exist. Refunds, receipts and accounts reporting remain. | Razorpay account and webhook |
| Notifications and email | In Progress | In-app rows and basic SMTP templates/delivery records exist. Transactional outbox, retries and preferences remain. | SMTP provider |
| API hardening | In Progress | CORS, headers, CSRF, secure production cookies, input models and selected rate limits are implemented. Full endpoint-by-endpoint authorization review and dependency remediation remain. | None |
| Database and migrations | Tested | Alembic history reaches `0005_permission_catalogue`; a clean PostgreSQL 16 container upgraded successfully to the head revision. Existing-production data migration and restore rehearsals remain. | Production backup and restore drill |
| Frontend | In Progress | Public pages and a basic role-aware portal build successfully. It does not contain all required dashboards or connected workflows. | Approved content/assets |
| Deployment | In Progress | Docker, Caddy and compose definitions parse; backend, migration and frontend production images build successfully. A deployed HTTPS environment is not yet verified. | Host, domain/DNS, TLS |
| Automated QA | In Progress | 16 backend tests, 2 frontend tests, lint, production frontend build, PostgreSQL migration and production image builds passed locally on 14 November 2026. Provider and full workflow checks remain. | Provider sandboxes |

## Files changed in this hardening pass

- Backend: `core.py`, `models.py`, `schemas.py`, `main.py`, `security.py`, `email_service.py`, `permissions.py`, `seed.py`, plus `sms_service.py`, `scanner_service.py`, migrations `0004_verification_mfa_recovery.py` and `0005_permission_catalogue.py`, and API tests.
- Frontend: ESLint dependency compatibility in `package.json` / `package-lock.json`.
- Operations: environment templates, production compose settings, Alembic import configuration, and the handover documents listed below.

## Verification record

- `python -m pytest -q` — 16 passed (two FastAPI lifecycle deprecation warnings).
- `npm test` — 2 passed; `npm run lint` and `npm run build` — passed.
- `alembic -c alembic.ini heads` — `0005_permission_catalogue (head)`; clean PostgreSQL 16 upgrade — passed.
- Compose syntax validation and final production Docker image builds — passed.

No production deployment, DNS update, payment, email or SMS was executed.
