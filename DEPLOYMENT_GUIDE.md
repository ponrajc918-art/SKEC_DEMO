# Deployment guide

This guide is a preparation runbook, not evidence of a completed deployment.

1. Provision a patched Linux host, private PostgreSQL 16 service, backup destination, DNS name and SMTP/SMS/Razorpay/ClamAV accounts as applicable.
2. Copy the source archive to the host. Create `.env.production` from `.env.production.example`; fill owner-controlled placeholders in the secret store or file with restrictive permissions.
3. Before any migration, create and verify a backup using `DATABASE_BACKUP_RESTORE.md`.
4. Validate the composition and apply migrations:

```bash
docker compose -f docker-compose.prod.yml --env-file .env.production config --quiet
docker compose -f docker-compose.prod.yml --env-file .env.production build
docker compose -f docker-compose.prod.yml --env-file .env.production run --rm migrate
docker compose -f docker-compose.prod.yml --env-file .env.production up -d
curl --fail https://YOUR_DOMAIN/api/v1/health
```

5. Confirm Caddy can obtain the certificate: ports 80 and 443 must be reachable and DNS must point to the host. Do not publish PostgreSQL ports.
6. Configure the Razorpay webhook to `https://YOUR_DOMAIN/api/v1/payments/webhook`; use the raw-body webhook secret in `RAZORPAY_WEBHOOK_SECRET`. Complete a test-mode payment and reconciliation only after owner approval.

The deployment is blocked until the missing ERP, PostgreSQL integration and Docker build verification listed in `SKEC_IMPLEMENTATION_TRACKER.md` is completed.
