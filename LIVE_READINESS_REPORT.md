# Live readiness report

## Delivery state

This archive is a source and deployment-configuration delivery, not a deployed public service. It includes a Next.js public site and portal, FastAPI API, Alembic migrations through `0003_live_services`, Docker production topology, and placeholder-only configuration.

Implemented server paths include account sign-in/out, secure cookies and CSRF checks, RBAC, password reset/change, invitation acceptance, login-attempt throttling/audit trail, TOTP enrolment/confirmation, mocked-or-SMTP transactional delivery, Razorpay order/signature/webhook handling, and private assignment-file storage with a scan-status release gate.

## Confirmed checks

- Eight backend integration tests passed in the supplied workspace.
- Alembic generated PostgreSQL SQL through the live-services migration.
- Production Compose configuration resolved successfully with placeholders only.

See `TEST_REPORT.md` for exact scope and omissions.

## Required before public launch

1. Put genuine secrets only in the deployment server's `.env.production` or a managed secret store: PostgreSQL password, session secret, Fernet key, SMTP secret, Razorpay test keys/webhook secret and final domain.
2. Build/start the production stack on a Linux host, confirm migrations and health endpoint, and perform browser smoke tests.
3. Test SMTP reset/invitation delivery to a controlled account.
4. Complete Razorpay **test-mode** checkout and webhook verification. Keep live payments disabled until finance approves a separate go-live.
5. Enrol MFA for privileged operational accounts, validate recovery procedures, then remove all demo accounts/data from the production database.
6. Connect a malware scanner for uploads, test clean/rejected flows, configure backups/restore, monitoring, incident response and privacy/retention policies.
7. Obtain SKEC approval for final factual content, contacts, branding assets, data controller and operating owner.

No credential is embedded in this archive, and no live email, payment, or public deployment claim is made.
