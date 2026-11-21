# Security review

## Fixed in this pass

- OTP verification now uses cryptographically generated six-digit codes, SHA-256 storage, expiry, one-time consumption, attempt limits, resend cooldown and destination/IP rate limiting.
- Unconfigured SMS delivery returns HTTP 503; it never claims a message was sent.
- MFA recovery codes are hashed and one-time use. Privileged accounts remain restricted to enrollment/security endpoints until MFA is confirmed in production.
- Private uploads are downloadable only after a configured ClamAV daemon reports them clean. Administrative users can no longer set an arbitrary `clean` value through an API.
- Protected endpoints now use a database-backed role/permission catalogue. Student/staff resource handlers explicitly reject accounts without the required profile record.
- Login throttling now limits failed attempts both by account identifier and by source IP.
- OTP hashes are keyed using the application session secret so a leaked verification table cannot be cheaply brute-forced offline.
- Production configuration rejects SQLite, wildcard/non-HTTPS CORS origins, insecure SMTP modes, unsupported/unconfigured SMS modes and invalid scanner configuration.
- SMTP exceptions are stored as a generic delivery failure rather than raw provider exception text.
- Direct Alembic CLI operation now sets the backend import path.

## Open security work

- Full RBAC/resource-ownership review, administrative recovery approval workflow, password history, reset throttling and a transaction outbox are not implemented.
- The generic SMS adapter must be mapped to a provider-approved request schema before production use.
- Full dependency scan found 15 npm advisories (10 moderate, 3 high, 2 critical), including Next/PostCSS, Zod and Vitest/Vite dependency paths. Production-only `npm audit --omit=dev` currently reports zero, but the full development supply chain still needs reviewed upgrades; no blanket `npm audit fix --force` was applied because it proposes breaking Next, Zod and Vitest upgrades.
- PostgreSQL-specific locking/constraint tests, container scanning, SAST/DAST and external penetration testing have not run.

## Operational rules

Never enable `PAYMENT_MODE=live`, publish a webhook, or expose upload services until the corresponding provider and scanner checks have passed. Treat the current application as not production-ready until the tracker’s blocked verification work is closed.
