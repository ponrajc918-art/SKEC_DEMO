# Environment setup

Copy `.env.example` to `.env` for local development and `.env.production.example` to `.env.production` only on the deployment host. Do not commit either completed file.

Required production values: `DOMAIN`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `SESSION_SECRET` (48+ random characters), `FIELD_ENCRYPTION_KEY`, `BACKEND_CORS_ORIGINS=https://<domain>`, `PUBLIC_SITE_URL=https://<domain>`, and `PRIVATE_STORAGE_ROOT`.

Optional integrations are enabled explicitly: set `EMAIL_MODE=smtp` plus SMTP settings for email; `SMS_PROVIDER=generic_http` plus `SMS_ENDPOINT`, `SMS_API_TOKEN` and `SMS_SENDER_ID` for SMS; `FILE_SCANNER_MODE=clamd` plus `CLAMD_HOST` for scanning; and Razorpay keys with `PAYMENT_MODE=test` first. `PAYMENT_MODE=live` also requires `ALLOW_LIVE_PAYMENTS=true`.

Generate a Fernet key with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`. Generate session secrets with a secure password manager or `python -c "import secrets; print(secrets.token_urlsafe(64))"`.
