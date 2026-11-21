# Provider setup guide

## Email

Use an organization-controlled transactional SMTP provider or Gmail Workspace with an App Password where eligible; normal Gmail passwords are not SMTP credentials. Set `EMAIL_MODE=smtp`, host, port, username, password, sender address and `SMTP_USE_TLS=true`. Send a single approved test message and verify the delivery record without exposing its contents.

## SMS

Select an India-compliant provider and approved sender/template. Map its endpoint to the generic JSON contract documented by `backend/app/sms_service.py` (`to`, `from`, `message`), then set `SMS_PROVIDER=generic_http`, endpoint, bearer token and sender ID. Until that mapping is validated, leave it `disabled`; mobile verification will return 503 safely.

## Razorpay

Create a Razorpay account, start with test keys, set `PAYMENT_MODE=test`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` and the independent webhook secret. Register the HTTPS webhook endpoint from the deployment guide. Move to live keys only after reconciliation and written approval; set `PAYMENT_MODE=live` and `ALLOW_LIVE_PAYMENTS=true` together.

## ClamAV

Run a private ClamAV daemon reachable from the backend, set `FILE_SCANNER_MODE=clamd`, `CLAMD_HOST` and port 3310. Test a benign file and a standard EICAR test file in a non-production environment. Do not expose ClamAV or private storage publicly.
