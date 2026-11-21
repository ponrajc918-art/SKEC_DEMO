# Test report

## 14 November 2026 verification update

- Backend: `python -m pytest -q` — **16 passed**; two FastAPI lifecycle deprecation warnings remain.
- Backend: Python compilation passed.
- Migrations: `alembic -c alembic.ini heads` resolves to `0005_permission_catalogue`; PostgreSQL SQL generation passes and emits account-verification columns only in their respective revisions.
- Frontend: `npm run lint` and `npm run build` passed.
- Frontend: `npm test` — **2 passed**; the initial unit tests cover protected portal endpoint mapping and CSRF-cookie parsing.
- PostgreSQL: a fresh PostgreSQL 16 container successfully applied migrations through `0005_permission_catalogue` and contained all three additional target roles.
- Containers: development and production Compose configurations parse; backend, migration and frontend production images build successfully.
- Dependency audit: full audit reports 15 advisories; production-only audit reports zero. See `SECURITY_REVIEW.md`.

## Historical baseline (superseded)

Executed on 2026-11-13 in the supplied Windows workspace; retained for traceability only. The verification update above is authoritative.

| Check | Result | Evidence |
|---|---|---|
| Backend integration tests | Passed | `python -m pytest -q` — 8 passed, including reset-token lifecycle, private-file access gate, Razorpay HMAC helpers and TOTP algorithm |
| Alembic migration SQL generation | Passed | `python -m alembic -c alembic.ini upgrade head --sql` generated the 0003 PostgreSQL DDL |
| Docker Compose syntax | Passed | `docker compose config` resolved all three services |
| Production Compose syntax | Passed | `docker compose -f docker-compose.prod.yml config` resolved Caddy, frontend, backend, migration and private PostgreSQL services |
| Production secret check | Passed | The runtime rejects a weak production session secret |
| Demo reset guard | Passed | Reset completed only with both explicit development safeguards against an isolated SQLite database |
| CSRF request guard | Passed | Stateful student assignment submission is denied without the session-linked CSRF token and accepted with it |
| Production configuration | Passed | Compose resolved the new SMTP, Razorpay, MFA and private-storage variables from placeholders only |

## Tested workflow coverage

The API tests start the application with a synthetic SQLite test database, seed it, validate portal authorization and CSRF, exercise a mocked password-reset lifecycle, verify the file-download scan/ownership gate, and validate payment/MFA cryptographic helper logic. No real message or payment is generated.

## Not executed

- Docker image build/start against a running PostgreSQL container
- Frontend type check and production build after the newest account-recovery pages: Windows file-lock/tar extraction failures prevented npm from restoring a clean local dependency tree in this session. The source is included and the Docker image remains the intended verification path.
- Playwright/browser accessibility tests
- Live Razorpay, SMTP/SMS, object storage, malware scanning, cryptography-backed MFA enrolment or webhook tests
- Manual responsive and assistive-technology review

These omissions are intentional disclosures, not passing claims. The project must not be considered production-ready on the basis of this report.
