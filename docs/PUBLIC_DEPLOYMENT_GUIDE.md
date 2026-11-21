# Public deployment guide

This archive is prepared for a single Linux server with Docker Compose and Caddy-managed HTTPS. It is not an instruction to expose the site until SKEC approves the content, data controller, domain and operating owner.

## Prerequisites

1. A supported Linux server with Docker Engine and Docker Compose Plugin installed.
2. A DNS `A` or `AAAA` record for the final hostname pointing to the server before launch.
3. Ports 80 and 443 reachable from the internet; Caddy uses them to issue and renew TLS certificates.
4. A verified domain and mail/payment/storage credentials if those optional integrations will be activated. None are required for the website and demo portal to start.

## Launch

1. Copy the archive to the server and unpack it.
2. Copy `.env.production.example` to `.env.production`, set the true `DOMAIN`, and generate a unique database password, a 48+ character session secret, and a Fernet `FIELD_ENCRYPTION_KEY`. Do not reuse development values.
3. From the project root, run:

   ```bash
   docker compose --env-file .env.production -f docker-compose.prod.yml config
   docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
   ```

4. Confirm `https://YOUR_DOMAIN/api/v1/health` returns a healthy response and inspect `docker compose -f docker-compose.prod.yml logs --tail=100`.
5. Configure regular encrypted PostgreSQL backups and verify a restore before admitting real users.

## Operating rules

- Production has no automatic demo seeding and does not create database tables at application startup. The `migrate` container applies Alembic revisions before the API begins.
- Only Caddy exposes ports 80 and 443. PostgreSQL and FastAPI remain private to the Compose network.
- Caddy obtains TLS certificates after DNS and firewall configuration are correct.
- Create real accounts through a reviewed institutional onboarding process; do not use the demo accounts or seed synthetic data in production.
- Keep `PAYMENT_MODE=test` and `ALLOW_LIVE_PAYMENTS=false` until Razorpay test orders, signature verification and webhooks have been exercised end-to-end. Live payments require a reviewed change and `ALLOW_LIVE_PAYMENTS=true`.
- Configure SMTP with an approved sender and app password/SMTP secret, then send a password-reset message to a controlled mailbox before inviting users.
- Privileged roles must enrol their TOTP authenticator using the authenticated MFA endpoint; complete that one-time setup before normal administrative work.
- Before accepting real uploads, connect an approved scanner and make its clean/rejected status update part of the operating process.

## Rollback and backup

Take a database backup before every release. Retain the previous image tags and copy of `.env.production` in the organisation's secret store. A rollback is a deployment operation paired with a database-migration compatibility review; do not drop volumes to roll back.
