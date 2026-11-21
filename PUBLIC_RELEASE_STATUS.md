# Public release status

## Archive readiness

This archive is ready to be deployed publicly through the included `docker-compose.prod.yml`, Caddy HTTPS configuration and deployment guide. It is not already published: publication needs an organisation-controlled server, a real domain/DNS record and generated production secrets.

## Required launch inputs

| Input | Why it is required |
|---|---|
| Domain and DNS record | Caddy issues and renews the public TLS certificate for the configured hostname. |
| Linux server with Docker Compose | Runs the isolated Caddy, frontend, backend and PostgreSQL services. |
| Unique `POSTGRES_PASSWORD` and 48+ character `SESSION_SECRET` | Protect database and session data. |
| Content/data-owner sign-off | Phase 0 recorded unresolved institutional facts and image approvals. |
| Backup/restore confirmation | Required before real student or staff data is entered. |

## Deliberately excluded from public launch

The live payment gateway, outbound email/SMS, private document storage and production data import are not enabled without the college's credentials, contracts, data-retention decisions and service-specific validation. The public site and protected portal can run without them.
