# Production go-live checklist

- [ ] Complete every open item in `SKEC_IMPLEMENTATION_TRACKER.md`; do not waive RBAC, ERP or PostgreSQL verification work.
- [ ] Review and remediate dependency advisories with tested upgrades.
- [ ] Verify migrations on a disposable PostgreSQL copy, then take and test a production backup.
- [ ] Configure HTTPS, CORS, secure cookies, DNS, backup retention and monitoring.
- [ ] Configure SMTP, SMS, ClamAV and Razorpay test mode; verify each without real bulk sends or charges.
- [ ] Complete MFA enrollment for every privileged account and retain recovery codes securely.
- [ ] Execute backend tests, frontend lint/build, Docker builds and a manual authorization test plan.
- [ ] Perform an external security assessment and obtain written owner authorization before live payments, DNS changes or public launch.

At present, these boxes are not complete; this repository must not be represented as launched or fully live-ready.
