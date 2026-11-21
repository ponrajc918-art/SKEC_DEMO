# Database backup and restore

Run these commands against the production database host; test every backup and restore on a separate PostgreSQL instance first.

```powershell
pg_dump --format=custom --no-owner --file skec-$(Get-Date -Format yyyyMMdd-HHmmss).dump $env:DATABASE_URL
pg_restore --list .\skec-YYYYMMDD-HHMMSS.dump
createdb skec_restore_test
pg_restore --clean --if-exists --no-owner --dbname skec_restore_test .\skec-YYYYMMDD-HHMMSS.dump
```

Never use `--clean` against the production database. Keep encrypted backups outside the application host, restrict access, define retention, and perform a documented restore drill before go-live. Migrations are applied with `docker compose -f docker-compose.prod.yml run --rm migrate`; take and verify a backup immediately before that step.
