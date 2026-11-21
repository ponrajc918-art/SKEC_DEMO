# Phase Roadmap

Phase 0 deliverable. Seven phases (0 to 6), one architecture. Each phase ends with: updated documentation, an updated downloadable ZIP, a report of tests **actually run** with their results, a list of what is not yet implemented, and a hard stop until the project owner approves.

## Working rules for every phase

1. The same repository and conventions throughout; no rewrite of working code.
2. A feature is "complete" only if implemented **and** tested **and** the test run is reported. Otherwise it is listed as partial or not started.
3. No invented college information. Placeholders and demo data are labelled; unverified facts follow CONTENT_VERIFICATION.md.
4. No GitHub operations; no secrets in any file.
5. No test result, build output or download link is ever fabricated. If the chat sandbox cannot run something, the report says so and states what was verified instead.
6. Do not start the next phase until the owner gives explicit approval.

## Execution reality in Claude Free chat

Work happens in a sandbox attached to the chat: files can be created and zipped, and package registries (npm, PyPI) are reachable, so dependency installation, type checks, unit tests and linting are expected to be runnable. Things that **may not** be runnable and will be probed at the start of each phase, then reported honestly: Docker builds and Compose, Playwright browsers (their downloads come from hosts outside the sandbox's allow-list), a local PostgreSQL server, outbound calls to Razorpay or an SMTP server, and visual review on real devices. Where something cannot run, the phase delivers the code and instructions but marks the feature **"implemented, not verified in this environment"**, never "complete".

---

## Phase 0: Foundation (this phase)

**Scope:** research, requirements, architecture, design system, page inventory, asset strategy, database plan, production planning, roadmap.

**Deliverables:** README.md, the ten documents in `docs/`, `.env.example`, `.gitignore`, folder skeleton, image manifests (Markdown and JSON), `scripts/validate_phase0.py`, `SKEC_Digital_Campus_Phase_0.zip`.

**Acceptance criteria**

- [x] All twelve required files exist.
- [x] Phases 0 to 6 are documented consistently across README, PROJECT_PROGRESS and this file.
- [x] Image replacement strategy documented, with manifest in two synchronised formats.
- [x] No secrets present (checked by script).
- [x] ZIP integrity tested.
- [ ] Owner approval (pending).

---

## Phase 1: Public website

**Goal:** a complete, professional, responsive public college website built on the design system, with branded placeholders and clearly marked demo content. No login, no database.

**Starts with:** (a) a content sweep of all NOT-INSPECTED pages listed in CONTENT_VERIFICATION.md, with the register updated; (b) a capability probe of the sandbox (npm install, build, test, Playwright).

**Scope**

- Scaffold Next.js, TypeScript, Tailwind, shadcn/ui, Lucide in `frontend/`, keeping the existing `public/images` folders and `image-manifest.json`.
- Tailwind tokens, fonts, global styles from DESIGN_SYSTEM.md.
- Components: header with mega-menu and mobile drawer, footer, breadcrumbs, `SiteImage`, `ImagePlaceholder`, cards, buttons, notice list, forms.
- All public pages in PAGE_INVENTORY.md section 1 (about, academics, admissions, placements, campus life, news and events, gallery, alumni, committees, contact), using typed content files.
- Enquiry and grievance forms: complete UI and client/server validation, submitting to a stub that clearly says "not yet connected" until Phase 2.
- SEO basics, sitemap, robots, 301 redirect map for legacy URLs, 404 page.
- Verification badges on any unconfirmed content (dev builds), and a build-time check that fails the production build if an unapproved item is marked as final.

**Acceptance criteria**

1. Every public page in the inventory exists (or is explicitly listed as deferred with a reason) and renders without errors.
2. Pages work from 320px to 1920px with no horizontal scrolling (checked by Playwright viewport tests if browsers are available; otherwise reported as not verified).
3. No empty image boxes: every image slot shows an approved image or a branded placeholder; the Chairman slot never shows a fabricated face.
4. Content registry check: every institutional fact in the build maps to a source and a status.
5. No invented names, statistics, placement figures or achievements anywhere.
6. Type check, lint and component tests pass, with output reported.
7. Automated accessibility checks pass on key pages (axe) where runnable; otherwise reported as not verified.
8. Lighthouse-style performance and accessibility numbers reported only if actually measured.
9. Documentation and PROJECT_PROGRESS.md updated; ZIP `SKEC_Digital_Campus_Phase_1.zip` produced and integrity-tested.

**Not in Phase 1:** database, authentication, ERP, payments.

---

## Phase 2: Backend foundation

**Goal:** the API, database and migration foundation, plus the first real persistence (enquiries and grievances).

**Scope**

- FastAPI project structure per ARCHITECTURE.md; settings, logging, error format, health endpoints.
- PostgreSQL and SQLAlchemy 2.x models for identity, organisation and website tables (DATABASE_PLAN.md 2.1, 2.2, 2.10).
- Alembic migrations (up and down), seeds for roles, permissions and grade scales.
- Enquiry and grievance endpoints with validation, rate limiting and spam protection; frontend forms connected.
- Dockerfiles, `compose.dev.yml`, reverse-proxy configuration.
- CI-ready test layout.

**Acceptance criteria**

1. `pytest` unit and API integration tests pass, with output reported.
2. Database integration tests run against a real PostgreSQL if the sandbox can host one; if not, they are written, marked **not run**, and the limitation is reported.
3. Migrations apply from empty and roll back cleanly (reported only if run).
4. OpenAPI schema generated; frontend uses a typed client.
5. Enquiry submission stores a row and returns a reference; invalid and abusive input rejected with tests.
6. No secrets in code; `.env.example` updated.
7. Docker files statically validated; if Docker cannot run here, the report says "not built in this environment".
8. ARCHITECTURE.md and DATABASE_PLAN.md reconciled with what was built; ZIP produced.

---

## Phase 3: Authentication, RBAC and portal shells

**Goal:** secure sign-in and role-aware portals with audit logging.

**Scope**

- Argon2id passwords, server-side sessions, CSRF protection, rate limiting, lockout.
- TOTP MFA, mandatory for principal, HOD, college admin and finance admin; recovery codes.
- Password reset and invitation flows (email sending stubbed until Phase 5; tokens fully implemented).
- Roles, permissions and scopes; the single `authorize()` function with a unit test for every rule.
- Audit log writing and an admin viewer.
- Portal shells (student, staff, HOD, principal, college admin) with navigation by permission and account/security pages.

**Acceptance criteria**

1. Authorisation test matrix: for each role and each protected endpoint, allowed and denied cases are tested; all pass (output reported).
2. A student cannot read another student's data; an HOD cannot read other departments' data; both proven by tests.
3. MFA enforced for privileged roles: login without second factor fails (tested).
4. Session fixation, expiry, revocation and CSRF behaviours tested.
5. Failed-login rate limiting and lockout tested.
6. Every sensitive action in scope writes an audit row (tested).
7. Passwords stored only as Argon2id hashes (tested); no secrets in logs (checked).
8. Playwright login journeys for each role if runnable; otherwise reported as not verified.
9. Documents updated; ZIP produced.

---

## Phase 4: Core ERP modules

**Goal:** the working academic and administrative modules.

**Scope (each with API, UI, tests):**

- Student and staff management, admissions, department/batch/section allocation.
- Timetable; attendance (marking, locking, amendments, summaries and thresholds).
- Assignments and submissions.
- Internal assessments, semester examinations, results, publication workflow.
- Question paper vault: private storage, role-restricted access, controlled download, full audit trail.
- Fees: structures, assignments, invoices, offline payment recording, receipts, reconciliation views (online payments come in Phase 5).
- Circulars and announcements; notification centre.
- Placement drives, internships, alumni records.
- Leave management and staff attendance.
- Website CMS for news, events, gallery and downloads; real data replaces demo content.
- Reports and dashboards per role.

**Acceptance criteria**

1. Each module has API integration tests covering happy paths, validation errors and authorisation denials; all pass with output reported.
2. Business rules unit-tested: attendance percentage and thresholds, mark limits, grade and CGPA calculation, receipt numbering, fee dues.
3. Result publication cannot be performed by unauthorised roles, and published results are immutable except through audited revisions (tested).
4. Question paper download requires permission, scope and valid grant, and writes an audit row (tested); direct storage URLs are not exposed.
5. Concurrency cases tested for receipt numbering and attendance locking.
6. Demo data is flagged and excluded from production by an automated check.
7. Role-by-role UI walkthrough scripted in Playwright if runnable; otherwise listed as not verified.
8. Documents updated; ZIP produced.

---

## Phase 5: Integrations and security hardening

**Goal:** online payments in test mode, notifications, hardened storage and security.

**Scope**

- `PaymentGateway` interface and Razorpay adapter: server-side order creation, signature verification, webhook verification, idempotency, reconciliation job, failure and retry handling. **Test mode only.**
- Email provider adapter, templated notifications, delivery tracking; SMS/WhatsApp only if the college requests it.
- Background worker and queue where needed.
- Virus scanning of uploads; download watermarking for question papers; storage lifecycle and encryption review.
- Security hardening: CSP and headers, dependency and static analysis, secrets review, rate-limit tuning, backup and restore procedure written and rehearsed where possible.
- Privacy tooling: data export and anonymisation procedures drafted.

**Acceptance criteria**

1. Payment flow tests with mocked gateway responses pass (success, failure, duplicate webhook, tampered signature, amount mismatch).
2. Real Razorpay sandbox calls are made only if outbound access and test credentials are available; otherwise reported as **not verified against the live gateway sandbox**. No claim of working live payments is ever made.
3. Live mode is impossible without an explicit configuration change and written college approval, and the switch is audited.
4. Email templates render and the adapter is tested against a local SMTP sink where possible.
5. Security checks (static analysis, dependency audit, header checks) run and results reported, with unresolved findings listed.
6. Upload scanning and signed URL behaviour tested.
7. Documents updated; ZIP produced.

---

## Phase 6: Verification, performance and delivery

**Goal:** the production-oriented release candidate.

**Scope**

- Full regression: backend, database, frontend, Playwright end-to-end per role.
- Accessibility pass (automated and a documented manual review), cross-browser and device checks as far as tooling allows.
- Performance: query review, indexes, caching, image optimisation, load test of critical paths (admissions, login, fee payment, result view).
- Bug fixing and cleanup; dependency and licence review.
- Deployment preparation: production Compose files, runbook, backup/restore guide, monitoring set-up guide, go-live checklist, rollback plan.
- Documentation: administrator guide, user guides per role, API reference, security notes, known limitations.
- Image replacement: if approved photographs exist, they are installed via the manifest; otherwise placeholders ship and the process is documented.
- Final ZIP `SKEC_Digital_Campus_Phase_6.zip` with a manifest of contents and checksums.

**Acceptance criteria**

1. Complete test report: counts of tests run, passed, failed and skipped, per layer, with logs. Failures are fixed or listed as known issues.
2. No critical or high severity open security findings; medium findings documented with owners.
3. Load-test results stated with the tool, scenario and environment (a sandbox result is labelled as such and is not a production capacity claim).
4. Go-live checklist complete except items that need the college (credentials, DNS, legal sign-off), which are listed explicitly.
5. All documents consistent with the code; PROJECT_PROGRESS.md final.
6. ZIP integrity verified.

---

## Dependency chain

```text
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
 foundation  public     backend    auth/RBAC   ERP        payments    verify,
             site       + DB                   modules    + hardening deliver
```

Phase 1 can proceed on demo and verified-site content. Phases 4 and 5 depend on information from the college (fee structures, regulations, grading rules, payment credentials) listed in CONTENT_VERIFICATION.md section 8 and DATABASE_PLAN.md section 8. Missing inputs delay those items; they are never filled with guesses.
