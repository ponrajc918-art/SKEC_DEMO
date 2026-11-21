# Image Asset Manifest

Status: photographs supplied by the project owner in `Skec.docx` are integrated (status `user-supplied`). Slots with no verified photograph remain placeholders. See `docs/IMAGE_INTEGRATION_REPORT.md` for the full placement and exclusion report.

The machine-readable twin of this table is `frontend/src/content/image-manifest.json`. The JSON is now the source of truth and is edited directly; `scripts/generate_asset_manifest.py` is the original Phase 0 generator and refuses to run (it would overwrite real image data).

## Rules

- Image collection is **not** a blocker for development. Slots render branded placeholders until a file is approved.
- No fabricated photographs, stock photos or AI-generated images pretending to be SKEC buildings, students, staff or events.
- The Founder Chairman portrait must be the genuine photograph supplied by the project owner. It is never generated, retouched beyond standard crop/exposure, or substituted.
- Pages reference images by **ID**, so replacing a file never requires editing a page.

## Status vocabulary

| Status | Meaning |
|---|---|
| `placeholder` | Branded CSS placeholder is shown. Official photograph not yet supplied. |
| `awaiting-user-supplied` | Needs a specific file that the project owner holds (Chairman portrait). |
| `awaiting-official` | Needs an official college asset (logo master, prospectus cover). |
| `user-supplied` | Genuine photograph supplied by the project owner is in place and shown on the site; college sign-off still pending. |
| `approved` | Official, rights-cleared photograph is in place and approved by the college. |

## Folder structure

```text
frontend/public/images/<category>/   served files (final, optimised)
frontend/src/content/image-manifest.json   registry used by pages
assets/incoming/                     untouched originals as received (not committed)
assets/placeholders/                 source artwork for branded placeholders (Phase 1)
```

## Image slots (39)

| ID | Category | Intended page | Filename (under `frontend/public/images/`) | Dimensions (px) | Alt text | Status |
|---|---|---|---|---|---|---|
| `brand.logo` | brand | Header, footer, favicon source | `brand/skec-logo.png` | 234 x 234 | Sri Krishna College of Engineering logo with the motto Talent, Technique and Training | user-supplied |
| `brand.og-image` | brand | Social sharing preview (all pages) | `brand/og-default.jpg` | 1200 x 630 | Sri Krishna Engineering College | placeholder |
| `chairman.portrait` | chairman | Founder Chairman page, home welcome block | `chairman/dr-r-vivekanandhan.jpg` | 581 x 538 | Portrait of Dr. R. Vivekanandhan, Founder Chairman, Sri Krishna Educational Trust | user-supplied |
| `home.hero` | hero | Home hero | `hero/skec-main-building-hero.jpg` | 1500 x 695 | Main academic building of Sri Krishna Engineering College with the college name on the roof | user-supplied |
| `home.facility-library` | hero | Home facilities strip | `library/library-reading-hall.jpg` | 1200 x 670 | Students reading at a large table in a college library | user-supplied |
| `home.facility-transport` | hero | Home facilities strip | `transport/college-buses.jpg` | 900 x 500 | Rows of yellow buses parked in a transport yard | user-supplied |
| `home.facility-hostel` | hero | Home facilities strip | `hostel/hostel-room.jpg` | 1200 x 798 | Hostel room with beds, study desks and wardrobes | user-supplied |
| `about.campus-overview` | about | About the college | `about/main-entrance-gate.jpg` | 1280 x 963 | Main entrance gate with the Sri Krishna Engineering College name board | user-supplied |
| `about.vision-banner` | about | Vision and mission | `about/vision-banner.jpg` | 1920 x 640 | Students on campus | placeholder |
| `about.leadership-banner` | about | Leadership and administration | `about/leadership-banner.jpg` | 1920 x 640 | College administrative block | placeholder |
| `campus.hero` | campus | Our campus | `hero/skec-main-building-hero.jpg` | 1500 x 695 | Main academic building of Sri Krishna Engineering College with the college name on the roof | user-supplied |
| `campus.infrastructure` | campus | Infrastructure | `campus/infrastructure.jpg` | 1600 x 900 | Academic block and grounds | placeholder |
| `dept.cse` | departments | Department: B.E. Computer Science and Engineering | `departments/dept-cse.jpg` | 1600 x 900 | Computer Science and Engineering department | placeholder |
| `dept.ece` | departments | Department: B.E. Electronics and Communication Engineering | `departments/dept-ece.jpg` | 1600 x 900 | Electronics and Communication Engineering department | placeholder |
| `dept.eee` | departments | Department: B.E. Electrical and Electronics Engineering | `departments/eee-electrical-machines-lab.jpg` | 768 x 404 | Students working around electrical machines in a laboratory | user-supplied |
| `dept.aids` | departments | Department: B.Tech. Artificial Intelligence and Data Science | `departments/dept-aids.jpg` | 1600 x 900 | Artificial Intelligence and Data Science department | placeholder |
| `dept.it` | departments | Department: B.Tech. Information Technology | `departments/it-computer-lab.jpg` | 533 x 400 | Students working at computers in a laboratory | user-supplied |
| `dept.ft` | departments | Department: B.Tech. Fashion Technology | `departments/dept-ft.jpg` | 1600 x 900 | Fashion Technology department | placeholder |
| `dept.mba` | departments | Department: M.B.A. | `departments/mba-lecture-hall.jpg` | 612 x 372 | A lecture in a tiered classroom with students seated at desks | user-supplied |
| `dept.me` | departments | PG programmes: M.E. (Applied Electronics, Computer Science) | `departments/me-machine-workshop.png` | 474 x 257 | Students operating lathe machines in a workshop | user-supplied |
| `admissions.banner` | admissions | Admissions, UG, PG | `admissions/admissions-banner.jpg` | 1920 x 640 | Admissions at SKEC | placeholder |
| `admissions.prospectus-cover` | admissions | Prospectus | `admissions/prospectus-cover.jpg` | 900 x 1200 | Prospectus cover | awaiting-official |
| `placements.hero` | placements | Placements and recruitments | `placements/placements-at-skec.jpg` | 960 x 400 | Group of students and graduates with raised arms, captioned Placements @ SKEC | user-supplied |
| `placements.internships` | placements | Internships | `placements/internships.jpg` | 1600 x 900 | Student internship activity | placeholder |
| `industry.banner` | industry | Industry interaction | `industry/industry-banner.jpg` | 1920 x 640 | Industry interaction session | placeholder |
| `hostel.hero` | hostel | Hostel facility | `hostel/hostel-room.jpg` | 1200 x 798 | Hostel room with beds, study desks and wardrobes | user-supplied |
| `hostel.room` | hostel | Hostel facility | `hostel/hostel-room.jpg` | 1200 x 800 | Hostel room interior | placeholder |
| `library.hero` | library | Library | `library/library-stacks.png` | 474 x 245 | Library stacks and study space | user-supplied |
| `sports.hero` | sports | Sports | `sports/volleyball-court.jpg` | 670 x 500 | Students playing volleyball on an outdoor court | user-supplied |
| `transport.hero` | transport | Transport facility | `transport/college-buses.jpg` | 900 x 500 | Rows of yellow buses parked in a transport yard | user-supplied |
| `canteen.hero` | canteen | Canteen | `canteen/canteen-dining-hall.jpg` | 1024 x 608 | Students seated at tables in a college dining hall | user-supplied |
| `cultural.hero` | cultural | Cultural activities | `cultural/aaravam-23-cultural-programme.jpg` | 1280 x 720 | Students performing on stage at a cultural programme under a banner reading Aaravam ’23 | user-supplied |
| `student-zone.hero` | student-zone | Student zone | `student-zone/student-zone-hero.jpg` | 1600 x 900 | Students at SKEC | placeholder |
| `events.default-card` | events | News and events cards (fallback) | `events/event-default.jpg` | 1200 x 800 | College event | placeholder |
| `events.fusion-2026` | events | News and events | `events/fusion-2-11-symposium-2026.jpg` | 756 x 503 | Guests seated on stage at the Fusion 2.11 National Level Technical Symposium | user-supplied |
| `labs.hero` | labs | Laboratories and facilities | `labs/computer-laboratory.jpg` | 1075 x 716 | Students at computers arranged along a long laboratory bench | user-supplied |
| `gallery.cover` | gallery | Gallery landing page | `gallery/gallery-cover.jpg` | 1600 x 900 | Gallery cover | placeholder |
| `alumni.hero` | alumni | Alumni | `alumni/alumni-hero.jpg` | 1600 x 900 | SKEC alumni | placeholder |
| `committees.hero` | committees | Committees and grievance | `committees/committees-hero.jpg` | 1600 x 640 | College committees | placeholder |

## Replacement instructions

1. Receive the official photograph and confirm in writing that the college approves its publication.
2. Place the untouched original in `assets/incoming/` (this folder is git-ignored apart from `.gitkeep`).
3. Crop to the aspect ratio in the table, export at the stated dimensions (and a 2x variant if needed) as JPEG or WebP, and save it to the exact path in the **Filename** column under `frontend/public/images/`.
4. Edit the matching entry in `frontend/src/content/image-manifest.json`: set `"status": "approved"`, add `"credit"` and `"approvedBy"`, and refine `"alt"` to describe the real photograph.
5. Re-run `python3 scripts/generate_asset_manifest.py` only if slots were added or removed; otherwise update this table's Status cell to match the JSON.
6. No page code changes are required: pages reference images by **ID** (for example `home.hero`), never by path. The `SiteImage` component (Phase 1) shows the branded placeholder until the status is `approved`.

## Alt text policy

- Describe what is visible, in one sentence, without keyword stuffing (the current official site stuffs alt text and page titles with search keywords; the new site must not).
- Decorative images use empty alt text.
- People are named only with their consent and verified identity.

## Consent and rights checklist (before status becomes `approved`)

- [ ] College approval recorded
- [ ] Photographer or source credit recorded
- [ ] Consent obtained where identifiable students (especially minors) or staff appear
- [ ] Image free of watermarks from third-party stock libraries
