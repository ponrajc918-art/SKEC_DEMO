# Project Progress

Updated at the end of every phase. Last update: **2026-11-13 (professional demonstration transformation delivered)**. The Phase 0 materials below remain as the baseline record; current implementation and test status are in `../FINAL_IMPLEMENTATION_REPORT.md`, `../PROFESSIONAL_TRANSFORMATION_REPORT.md` and `../TEST_REPORT.md`.

## Current implementation update

The original Phase 0 status table below is historical. The active project now includes a Next.js public website, FastAPI API, protected role-aware portal, local demo seed, two migrations, Docker configuration and verified integration tests. The professional transformation added role-specific portal navigation and API-backed demo workflows for timetable data, assignment submissions, notifications, profile changes and administration. External services and production release controls remain explicitly limited in `../KNOWN_LIMITATIONS.md`.

## 1. Phase status

| Phase | Name | Status | Notes |
|---|---|---|---|
| 0 | Foundation: research, architecture, design system | **Delivered, awaiting approval** | Documents and folder skeleton only; no application code |
| 1 | Public website | Not started | Will not begin until Phase 0 is approved |
| 2 | Backend foundation (FastAPI, PostgreSQL, migrations) | Not started | |
| 3 | Authentication, RBAC, portals, audit logs | Not started | |
| 4 | Core ERP modules | Not started | |
| 5 | Integrations and security hardening | Not started | |
| 6 | Testing, performance, deployment preparation, final delivery | Not started | |

## 2. What exists after Phase 0

| Item | State |
|---|---|
| Documentation (10 files in `docs/`, plus README) | Written |
| `.env.example`, `.gitignore` | Written (placeholders only) |
| Folder skeleton (frontend, backend, deployment, assets, scripts) | Created |
| Image manifest (38 slots, Markdown and JSON, generated from one script) | Created; no real images |
| Validation script `scripts/validate_phase0.py` | Written and run (see section 4) |
| Website, ERP, backend, database, tests, Docker files | **Not implemented** |

## 3. Phase 0 task checklist

| Task | Status | Evidence / limits |
|---|---|---|
| A. Research of public official site | Partly complete | 15 official pages and one PDF read; 18 linked pages and several PDFs **not inspected** (listed in CONTENT_VERIFICATION.md section 2) |
| B. Architecture | Complete (as a design) | ARCHITECTURE.md |
| C. Design system | Complete (as a specification) | DESIGN_SYSTEM.md; contrast ratios computed; not visually tested |
| D. Page inventory | Complete | PAGE_INVENTORY.md |
| E. Asset architecture | Complete | Folder tree, manifest, replacement steps |
| F. Database planning | Complete (as a plan) | DATABASE_PLAN.md |
| G. Production planning | Complete | PRODUCTION_COSTS.md; no prices quoted |
| H. Roadmap and acceptance criteria | Complete | PHASE_ROADMAP.md |

## 4. Phase 0 checks executed

Run with `python3 scripts/validate_phase0.py` from the project root. The results are reproduced in the Phase 0 final report. The script checks: required files exist, required headings exist, all seven phases are named in README, PROGRESS and ROADMAP, relative Markdown links resolve, image manifest JSON and Markdown agree, `.env.example` holds placeholders only, and no secret-like strings appear anywhere. It does **not** check the truth of institutional facts; that is a human review.

## 5. Decisions log

| ID | Date | Decision | Reason |
|---|---|---|---|
| D-01 to D-08 | 2026-11-13 | See ARCHITECTURE.md section 16 | Initial architecture |
| D-09 | 2026-11-13 | Images stored under `frontend/public/images/<category>/`, referenced by ID through `image-manifest.json` | Pages never contain image paths; replacement needs no code change |
| D-10 | 2026-11-13 | Gold used as accent; `gold-700` for text on light backgrounds | `#9A7B3F`-style golds fail AA contrast (computed 3.98:1) |
| D-11 | 2026-11-13 | Unconfirmed facts are labelled and excluded from production builds | Project rule 7 and 8 |
| D-12 | 2026-11-13 | Do not republish anything from the existing Mandatory Disclosure PDF | Outdated and contains personal data (V-09) |

## 6. Open questions and blockers

| # | Item | Blocks | Owner |
|---|---|---|---|
| Q-01 | Approved programme list and intake (conflict C-01) | Phase 1 department pages | College |
| Q-02 | Official contact emails (C-02) | Phase 1 contact page | College |
| Q-03 | Approved Chairman biography and portrait file | Phase 1 chairman page | Project owner and college |
| Q-04 | Status of `online.skec.edu.in` (V-11) | Student login link | College IT |
| Q-05 | Current 2026-2027 admission eligibility and fees (V-01) | Phase 1 admissions pages | College |
| Q-06 | Does the platform cover SKIT as well? (C-05) | Phase 2 data model | College |
| Q-07 | Hosting, operator, budget and uptime expectations | Phase 5 | Project owner and college |
| Q-08 | Razorpay account holder and approval for live mode | Phase 5 | College |
| Q-09 | Inspect the 18 not-yet-inspected official pages | Start of Phase 1 | Claude, at Phase 1 start |

## 7. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Official site content is stale or conflicting | Publishing wrong facts about the college | Register, publication gate, build-time check |
| Sandbox cannot run Docker, Playwright or PostgreSQL | Some tests cannot be proven here | Probe each phase, report honestly, label "not verified" |
| Sensitive student data and minors | Privacy and legal exposure | Data minimisation, RBAC, audit, legal review (Phase 5 gate) |
| Payment errors | Financial and reputational harm | Test mode first, idempotency, reconciliation, written approval for live |
| Missing college inputs (fees, regulations) | Delay in Phase 4 and 5 | List requirements early (CONTENT_VERIFICATION.md section 8) |
| Scope size for a chat-based workflow | Long phases | Strict per-phase stop and ZIP hand-off |

## 8. Known issues after Phase 0

1. Eighteen linked official pages and several PDFs were not inspected.
2. `online.skec.edu.in` returned a hosting default page when fetched; its true status is unknown.
3. The Prospectus is images only, so its text is not captured.
4. No visual design has been rendered; the design system is untested in a browser.
5. Docker, PostgreSQL and the application stack have not been built or run, because no application code exists yet.

## 9. Change log

| Date | Phase | Change |
|---|---|---|
| 2026-11-13 | 0 | Initial foundation created |
