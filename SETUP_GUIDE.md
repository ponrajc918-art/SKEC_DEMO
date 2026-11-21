# Local setup

## Recommended: Docker Compose

1. Copy `.env.example` to `.env` and replace all placeholders with local development values.
2. From the project root run `docker compose up --build`.
3. Open `http://localhost:3000`; API documentation is at `http://localhost:8000/api/docs`.

The development database starts with explicitly labelled synthetic demo data. See [demo accounts](docs/DEMO_ACCOUNTS.md).

## Direct development

Use Python 3.12 and Node 22 or newer. In `backend`, create a virtual environment, install `requirements.txt`, set `DATABASE_URL` to a local PostgreSQL database and run `uvicorn app.main:app --reload`. In `frontend`, run `npm install` then `npm run dev`.

Run Alembic migrations with `alembic upgrade head` from `backend`. This archive includes an initial migration; the local development startup creates schema only as a convenience and production must use Alembic.

## Reset the demonstration database

The reset mechanism is deliberately blocked unless both explicit safeguards are set. It drops and recreates only the configured **development** database, then loads synthetic records. Never point it at production.

```powershell
$env:APP_ENV="development"
$env:ALLOW_DEMO_RESET="YES_RESET_DEMO"
python scripts/reset_demo.py
```
