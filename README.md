# SKEC Digital Campus

> Current status: **not production-ready**. The repository contains a limited prototype plus ongoing security hardening, not the complete ERP defined in the handover brief. Read [SKEC_IMPLEMENTATION_TRACKER.md](SKEC_IMPLEMENTATION_TRACKER.md), [SECURITY_REVIEW.md](SECURITY_REVIEW.md), and [PRODUCTION_GO_LIVE_CHECKLIST.md](PRODUCTION_GO_LIVE_CHECKLIST.md) before deployment.

> Current delivery: a deployment-configuration-ready public site and campus-platform source archive with a Next.js website, FastAPI API, role-aware portal, Alembic migrations, Docker production topology and tested API workflows. It is not yet a deployed public service. See [LIVE_READINESS_REPORT.md](LIVE_READINESS_REPORT.md), [SETUP_GUIDE.md](SETUP_GUIDE.md), [docs/PUBLIC_DEPLOYMENT_GUIDE.md](docs/PUBLIC_DEPLOYMENT_GUIDE.md), [TEST_REPORT.md](TEST_REPORT.md) and [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).

A new, independent project to build a professional website and ERP for **Sri Krishna Engineering College (SKEC)**, Panapakkam, Chennai.

- Official college website: https://skec.edu.in/
- Existing student portal: https://online.skec.edu.in/ (not connected, not modified)

> **Current status: integrated local implementation delivered.** The Phase 0 materials remain as a documented baseline; see [FINAL_IMPLEMENTATION_REPORT.md](FINAL_IMPLEMENTATION_REPORT.md), [TEST_REPORT.md](TEST_REPORT.md) and [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for the current, evidence-based status.

## What this repository will contain

**Public website:** home, about, history, vision and mission, Founder Chairman, leadership, academics, departments, faculty, curriculum and regulations, admissions, UG and PG programmes, prospectus, examination information, placements, recruitments and internships, industry interaction, campus life (infrastructure, hostel, library, sports, transport, canteen, cultural), student zone, news and events, circulars, gallery, alumni, committees, grievance, contact and enquiry.

**Authenticated portals (later phases):** student, staff, HOD, principal and college administration.

## Technology (planned)

| Layer | Choice |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Lucide icons |
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL (never accessed by the browser) |
| Security | Argon2id, secure sessions, RBAC, backend authorisation, MFA for privileged roles, audit logs |
| Infrastructure | Docker, Docker Compose, environment configuration, private object storage |
| Testing | Pytest, Playwright, API and database integration tests, frontend component tests |
| Payments | Razorpay adapter in Phase 5, test mode first |

## Roadmap

| Phase | Goal |
|---|---|
| 0 | Research, requirements, architecture, design system, project foundation (**this delivery**) |
| 1 | Complete public-facing college website |
| 2 | Backend foundation: PostgreSQL, FastAPI, SQLAlchemy, migrations |
| 3 | Authentication, RBAC, portals, sessions, audit logs |
| 4 | Core ERP modules: academics, attendance, assignments, examinations, fees, circulars, placements |
| 5 | Integrations, payment gateway test mode, notifications, secure storage, hardening |
| 6 | Full testing, bug fixes, performance, deployment preparation, documentation, final ZIP |

Each phase stops for explicit approval before the next begins. Details and acceptance criteria: [docs/PHASE_ROADMAP.md](docs/PHASE_ROADMAP.md).

## Folder structure

```text
skec-digital-campus/
  README.md
  .env.example                 placeholders only, never real secrets
  .gitignore
  docs/
    ARCHITECTURE.md
    DESIGN_SYSTEM.md
    PAGE_INVENTORY.md
    ASSET_MANIFEST.md
    CONTENT_VERIFICATION.md
    DATABASE_PLAN.md
    PROJECT_PROGRESS.md
    PRODUCTION_COSTS.md
    PHASE_ROADMAP.md
  frontend/                    Next.js app (Phase 1)
    public/images/<category>/  served images
    src/content/image-manifest.json
  backend/                     FastAPI app (Phase 2)
  deployment/                  Docker and proxy configuration (Phase 2 onward)
  assets/
    incoming/                  untouched originals as received (not committed)
    placeholders/              source art for placeholders
  scripts/
    generate_asset_manifest.py
    validate_phase0.py
```

## Reading order

1. [docs/PHASE_ROADMAP.md](docs/PHASE_ROADMAP.md): what happens when
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): how it is built
3. [docs/CONTENT_VERIFICATION.md](docs/CONTENT_VERIFICATION.md): what is verified, conflicting, outdated or missing
4. [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) and [docs/PAGE_INVENTORY.md](docs/PAGE_INVENTORY.md)
5. [docs/DATABASE_PLAN.md](docs/DATABASE_PLAN.md), [docs/PRODUCTION_COSTS.md](docs/PRODUCTION_COSTS.md), [docs/ASSET_MANIFEST.md](docs/ASSET_MANIFEST.md)
6. [docs/PROJECT_PROGRESS.md](docs/PROJECT_PROGRESS.md): current status, open questions, risks

## Permanent project rules (summary)

1. One consistent application and architecture across all phases; no unnecessary rewrites; working code is preserved.
2. No GitHub operations and no repository connections.
3. A feature is complete only when implemented **and** tested; test results are never fabricated.
4. No invented college information, staff details, student records, placement statistics or achievements. Verified facts, unverified facts, placeholders and demo data are always distinguished.
5. Free and open-source technology wherever practical; production hosting and services still cost money (see PRODUCTION_COSTS.md).
6. No secrets in code, documents or archives.
7. Documentation and progress are updated after every phase; each phase ships a ZIP.
8. No phase begins before the previous one is approved.

## Images

Photographs are deliberately **not** a blocker. Pages use branded placeholders and reference images by ID; real, approved photographs are dropped in at the end through the manifest. The Founder Chairman portrait is the genuine photograph supplied by the project owner and is never generated or altered. See [docs/ASSET_MANIFEST.md](docs/ASSET_MANIFEST.md).

## Environment

Copy `.env.example` to `.env` and replace every `__PLACEHOLDER__`. Never commit `.env`.

## Checks

```bash
python3 scripts/validate_phase0.py
```

Validates the Phase 0 deliverables. It does not verify institutional facts; see CONTENT_VERIFICATION.md.

## Limitations of the working environment

The project is built through Claude Free chat with uploaded archives and downloadable files. Docker, a local PostgreSQL server and browser-based tests may not be runnable in that environment. Each phase report states exactly what was run and what was not.
