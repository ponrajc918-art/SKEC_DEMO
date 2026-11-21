# Page Inventory

Phase 0 deliverable. Lists every planned page. **None is built yet.** "Legacy URL" is the path on the current official site (https://skec.edu.in). "Verification" uses the vocabulary of CONTENT_VERIFICATION.md. Content never appears as final until its source is approved by the college.

Phase column: the phase in which the page is built. Public pages are built in Phase 1 with content files; data-driven versions arrive later where stated.

## 1. Public website (Phase 1 unless stated)

| # | New route | Page | Legacy URL | Content source and verification | Notes |
|---|---|---|---|---|---|
| 1 | `/` | Home | `/` | Mixed. Contact and admission banner VERIFIED-SITE; events and news demo; recruiter logos UNVERIFIED | Hero, admissions strip, programmes, facilities, news, events |
| 2 | `/about` | About the college | `/Aboutus` | Site text exists; history USER-SUPPLIED and site-consistent; programme counts CONFLICT (C-01) | Rewritten, not copied |
| 3 | `/about/history` | History | part of `/Aboutus` | USER-SUPPLIED history H-01 to H-05, pending confirmation | Timeline with verification badges |
| 4 | `/about/vision-mission` | Vision and mission | `/Vision` | VERIFIED-SITE | Trust-level vision and mission |
| 5 | `/about/founder-chairman` | Founder Chairman (Dr. R. Vivekanandhan, Founder Chairman, Sri Krishna Educational Trust) | `/Founder` | Name and designation USER-SUPPLIED and VERIFIED-SITE; qualification line CONFLICT (C-03); superlatives UNVERIFIED | Dedicated 4:5 portrait slot (genuine photo to be supplied) |
| 6 | `/about/leadership` | Leadership and administration | `/Administration` | MISSING (no roster on site) | Trust objects are available; names need confirmation |
| 7 | `/academics` | Academics overview | `/Curriculum`, `/Department` | VERIFIED-SITE for programme list; CONFLICT C-01 | |
| 8 | `/academics/departments` | Departments | `/Department` | CONFLICT C-01 | Directory of 6 UG and PG programmes, as confirmed |
| 9 | `/academics/departments/[slug]` | Department detail (one per programme) | `/UnderGraduate`, `/PostGraduate` | Vision and mission VERIFIED-SITE; faculty, labs, outcomes NOT-INSPECTED/MISSING | Slugs: `cse`, `ece`, `eee`, `ai-ds`, `it`, `fashion-technology`, `mba`, `me-applied-electronics`, `me-cse`, and `me-ai-ds` only if confirmed |
| 10 | `/academics/faculty` | Faculty | PDF `AU-CAISTAFF-PhotoList.pdf` | NOT-INSPECTED | Phase 1 placeholder directory; Phase 4 data-driven |
| 11 | `/academics/curriculum` | Curriculum and syllabus | `/Curriculum` | VERIFIED-SITE (Regulation-2025 links) | Links to syllabus PDFs after link check |
| 12 | `/academics/regulations` | Academic regulations | `/Academic` | NOT-INSPECTED | C-04 to resolve |
| 13 | `/academics/examinations` | Examination information | `/Examination` | VERIFIED-SITE (titles only); C-04 | Timetable downloads |
| 14 | `/academics/circulars` | Circulars and announcements | `/Circular` | MISSING (V-07) | Empty state design; Phase 4 data-driven |
| 15 | `/admissions` | Admissions overview | `/Admissions` | NOT-INSPECTED (banner VERIFIED-SITE) | |
| 16 | `/admissions/undergraduate` | UG programmes and how to apply | `/UnderGraduate` | Eligibility OUTDATED (V-01); how-to-apply VERIFIED-SITE | Needs 2026-2027 data |
| 17 | `/admissions/postgraduate` | PG programmes and how to apply | `/PostGraduate` | VERIFIED-SITE; C-01 | |
| 18 | `/admissions/lateral-entry` | Lateral entry | part of `/UnderGraduate` | VERIFIED-SITE, dated | Needs current confirmation |
| 19 | `/admissions/prospectus` | Prospectus | `/Prospectus` | Images only (V-12) | Accessible version needs source document |
| 20 | `/admissions/enquiry` | Admission enquiry form | `/Enquiry` | NOT-INSPECTED | UI in Phase 1; storage and email in Phase 2 and 5 |
| 21 | `/placements` | Placements and recruitments | `/Recruitments` | Description VERIFIED-SITE; statistics MISSING (V-08) | No numbers until supplied |
| 22 | `/placements/internships` | Recruitments and internships | `/Internships` | NOT-INSPECTED | |
| 23 | `/placements/industry` | Industry interaction | `/Industry` | NOT-INSPECTED; recruiter claims UNVERIFIED (V-04) | |
| 24 | `/campus` | Campus overview | `/Ourcampus` | NOT-INSPECTED | |
| 25 | `/campus/infrastructure` | Infrastructure and laboratories | `/Infrastructure` | NOT-INSPECTED | |
| 26 | `/campus/hostel` | Hostel | `/Hostel` | Teaser VERIFIED-SITE; details NOT-INSPECTED | |
| 27 | `/campus/library` | Library | `/Library` | Teaser only | |
| 28 | `/campus/sports` | Sports | `/Sports` | NOT-INSPECTED | |
| 29 | `/campus/transport` | Transport | `/Transport` | Teaser VERIFIED-SITE (timings); routes NOT-INSPECTED | |
| 30 | `/campus/canteen` | Canteen | not in navigation | MISSING | Requested by the brief; confirm content exists |
| 31 | `/campus/cultural` | Cultural activities | `/Cultural` | NOT-INSPECTED | |
| 32 | `/campus/student-zone` | Student zone | `/Student` | NOT-INSPECTED | |
| 33 | `/news-events` | News and events listing | `/Events` | NOT-INSPECTED; demo content only | Data-driven from Phase 4 |
| 34 | `/news-events/[slug]` | News or event detail | none | PLACEHOLDER | |
| 35 | `/gallery` | Gallery | `/Gallery` | NOT-INSPECTED | Albums from CMS (Phase 4) |
| 36 | `/alumni` | Alumni | `/Alumni` | NOT-INSPECTED | Registration form later |
| 37 | `/committees` | Committees overview | `/Grivance` (partial) | NOT-INSPECTED | Statutory committees to be confirmed |
| 38 | `/committees/grievance` | Online grievance | `/Grivance` | NOT-INSPECTED | Form UI Phase 1; persistence Phase 2; workflow Phase 4 |
| 39 | `/contact` | Contact and enquiry | `/Contact` | VERIFIED-SITE; email CONFLICT C-02 | Map embed after confirming location |
| 40 | `/mandatory-disclosure` | Mandatory disclosure and statutory documents | PDFs | Existing PDF OUTDATED (V-09) | Page waits for current documents |
| 41 | `/privacy`, `/terms`, `/accessibility` | Policy pages | none | To be drafted; need legal review | |
| 42 | `/sitemap`, `/not-found`, `/error` | Utility pages | none | n/a | 404 and 500 designed in Phase 1 |

"Selfie Spot" (`/Selfies`) from the legacy navigation is not carried over unless the college asks for it.

### Legacy URL redirects

Every legacy path above redirects (301) to its new route. Misspelt legacy paths such as `/Grivance` are preserved only as redirects.

## 2. Authenticated portals (built in Phases 3 and 4; Phase 0 only plans them)

### 2.1 Shared pages (all roles)

| Route | Page | Phase |
|---|---|---|
| `/login` | Sign in | 3 |
| `/login/mfa` | Second-factor challenge | 3 |
| `/forgot-password`, `/reset-password` | Password reset | 3 |
| `/account/profile` | My profile | 3 |
| `/account/security` | Password, MFA, active sessions | 3 |
| `/notifications` | Notification centre | 4 |

### 2.2 Student portal (`/student/...`)

| Page | Purpose | Phase |
|---|---|---|
| Dashboard | Timetable today, attendance summary, announcements, dues | 4 |
| Profile and academic record | Personal and enrolment details | 3 and 4 |
| Attendance | Subject-wise attendance | 4 |
| Timetable | Weekly timetable | 4 |
| Assignments | View, submit, track | 4 |
| Internal marks | Internal assessment results | 4 |
| Semester results | Published results | 4 |
| Fees | Fee statement, pay (test mode first), receipts | 4 and 5 |
| Circulars | Announcements and downloads | 4 |
| Placement and internships | Opportunities and applications | 4 |
| Grievances | Raise and track | 4 |

### 2.3 Staff portal (`/staff/...`)

| Page | Purpose | Phase |
|---|---|---|
| Dashboard | Today's classes, pending tasks | 4 |
| Profile | Own details | 3 |
| My classes and timetable | Assigned offerings | 4 |
| Mark attendance | Per session | 4 |
| Assignments | Create, review, grade | 4 |
| Internal assessment | Enter marks | 4 |
| Leave | Apply and track | 4 |
| Staff attendance | Own record | 4 |
| Circulars | Read | 4 |
| Question papers | Upload and view only where permitted | 4 |

### 2.4 HOD portal (`/hod/...`)

| Page | Purpose | Phase |
|---|---|---|
| Department dashboard | Attendance, results, pending approvals | 4 |
| Staff in department | Assignments, workload | 4 |
| Leave approvals | Approve or reject | 4 |
| Timetable management | Department timetable | 4 |
| Student progress | Attendance and marks by batch | 4 |
| Department reports | Export | 4 |
| Question paper oversight | Scoped access | 4 |

### 2.5 Principal portal (`/principal/...`)

| Page | Purpose | Phase |
|---|---|---|
| Institution dashboard | Admissions, attendance, results, fee collection overview | 4 |
| Approvals | Leave and escalations | 4 |
| Reports | Cross-department reports | 4 |
| Circular approval | Publish institution circulars | 4 |
| Audit view (read only) | Review of sensitive actions | 4 |

### 2.6 College administration portal (`/admin/...`)

| Page | Purpose | Phase |
|---|---|---|
| Dashboard | System and operations overview | 3 and 4 |
| Users and roles | Create users, assign roles and scopes | 3 |
| Audit logs | Search and export | 3 |
| Organisation set-up | Departments, programmes, regulations, academic years, batches, sections | 4 |
| Student records | Admissions and enrolment | 4 |
| Staff records | Profiles, department assignment | 4 |
| Fee structures and collection | Define fees, view payments, reconcile | 4 and 5 |
| Examination cell | Schedules, marks publication, results | 4 |
| Question paper vault | Controlled upload, access grants, download log | 4 |
| Communication | Circulars, announcements, email campaigns | 4 and 5 |
| Placement and alumni | Drives, internships, records | 4 |
| Website content (CMS) | News, events, gallery, downloads, grievances | 4 |
| Enquiries | Public enquiry inbox | 2 and 4 |
| Reports | Standard reports and exports | 4 |
| System settings | Integrations, test/live payment mode switch (guarded) | 5 |

### 2.7 Portal system pages

403 (forbidden), 404, session-expired, maintenance, and an "MFA required" enrolment page for privileged roles.

## 3. Counts

- Public website: 42 numbered entries, expanding to about 60 routes once per-department and per-event pages are counted.
- Portals: 6 shared pages plus roughly 11 student, 10 staff, 7 HOD, 5 principal and 15 administration pages.

These are planning counts, and the counts will change as the college confirms the content.
