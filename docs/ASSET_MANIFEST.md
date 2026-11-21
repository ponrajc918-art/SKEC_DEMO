# Image Asset Manifest

Phase 0 deliverable. Status: **no real photographs are included**. Every slot below is a placeholder or is awaiting a supplied file.

The machine-readable twin of this table is `frontend/src/content/image-manifest.json`. Both are generated from `scripts/generate_asset_manifest.py` so they cannot drift apart.

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
| `approved` | Official, rights-cleared photograph is in place and approved by the college. |

## Folder structure

```text
frontend/public/images/<category>/   served files (final, optimised)
frontend/src/content/image-manifest.json   registry used by pages
assets/incoming/                     untouched originals as received (not committed)
assets/placeholders/                 source artwork for branded placeholders (Phase 1)
```

## Image slots (38)

| ID | Category | Intended page | Filename (under `frontend/public/images/`) | Dimensions (px) | Aspect | Alt text (draft) | Status |
|---|---|---|---|---|---|---|---|
| `brand.logo` | brand | Header, footer, favicon source | `brand/skec-logo.svg` | 512 x 512 | 1:1 | Sri Krishna Engineering College logo | awaiting-official |
| `brand.og-image` | brand | Social sharing preview (all pages) | `brand/og-default.jpg` | 1200 x 630 | 1.91:1 | Sri Krishna Engineering College | placeholder |
| `chairman.portrait` | chairman | Founder Chairman page, home welcome block | `chairman/dr-r-vivekanandhan.jpg` | 800 x 1000 | 4:5 | Portrait of Dr. R. Vivekanandhan, Founder Chairman, Sri Krishna Educational Trust | awaiting-user-supplied |
| `home.hero` | hero | Home hero | `hero/home-hero.jpg` | 1920 x 1080 | 16:9 | Sri Krishna Engineering College campus | placeholder |
| `home.facility-library` | hero | Home facilities strip | `hero/home-facility-library.jpg` | 1200 x 800 | 3:2 | College library reading area | placeholder |
| `home.facility-transport` | hero | Home facilities strip | `hero/home-facility-transport.jpg` | 1200 x 800 | 3:2 | College transport buses | placeholder |
| `home.facility-hostel` | hero | Home facilities strip | `hero/home-facility-hostel.jpg` | 1200 x 800 | 3:2 | College hostel building | placeholder |
| `about.campus-overview` | about | About the college | `about/campus-overview.jpg` | 1600 x 900 | 16:9 | Aerial or wide view of the SKEC campus | placeholder |
| `about.vision-banner` | about | Vision and mission | `about/vision-banner.jpg` | 1920 x 640 | 3:1 | Students on campus | placeholder |
| `about.leadership-banner` | about | Leadership and administration | `about/leadership-banner.jpg` | 1920 x 640 | 3:1 | College administrative block | placeholder |
| `campus.hero` | campus | Our campus | `campus/campus-hero.jpg` | 1920 x 800 | 12:5 | Main campus view | placeholder |
| `campus.infrastructure` | campus | Infrastructure | `campus/infrastructure.jpg` | 1600 x 900 | 16:9 | Academic block and grounds | placeholder |
| `dept.cse` | departments | Department: B.E. Computer Science and Engineering | `departments/dept-cse.jpg` | 1600 x 900 | 16:9 | Computer Science and Engineering department | placeholder |
| `dept.ece` | departments | Department: B.E. Electronics and Communication Engineering | `departments/dept-ece.jpg` | 1600 x 900 | 16:9 | Electronics and Communication Engineering department | placeholder |
| `dept.eee` | departments | Department: B.E. Electrical and Electronics Engineering | `departments/dept-eee.jpg` | 1600 x 900 | 16:9 | Electrical and Electronics Engineering department | placeholder |
| `dept.aids` | departments | Department: B.Tech. Artificial Intelligence and Data Science | `departments/dept-aids.jpg` | 1600 x 900 | 16:9 | Artificial Intelligence and Data Science department | placeholder |
| `dept.it` | departments | Department: B.Tech. Information Technology | `departments/dept-it.jpg` | 1600 x 900 | 16:9 | Information Technology department | placeholder |
| `dept.ft` | departments | Department: B.Tech. Fashion Technology | `departments/dept-ft.jpg` | 1600 x 900 | 16:9 | Fashion Technology department | placeholder |
| `dept.mba` | departments | Department: M.B.A. | `departments/dept-mba.jpg` | 1600 x 900 | 16:9 | Management Studies department | placeholder |
| `dept.me` | departments | PG programmes: M.E. (Applied Electronics, Computer Science) | `departments/dept-me.jpg` | 1600 x 900 | 16:9 | Postgraduate engineering programmes | placeholder |
| `admissions.banner` | admissions | Admissions, UG, PG | `admissions/admissions-banner.jpg` | 1920 x 640 | 3:1 | Admissions at SKEC | placeholder |
| `admissions.prospectus-cover` | admissions | Prospectus | `admissions/prospectus-cover.jpg` | 900 x 1200 | 3:4 | Prospectus cover | awaiting-official |
| `placements.hero` | placements | Placements and recruitments | `placements/placements-hero.jpg` | 1920 x 800 | 12:5 | Training and Placement Cell activity | placeholder |
| `placements.internships` | placements | Internships | `placements/internships.jpg` | 1600 x 900 | 16:9 | Student internship activity | placeholder |
| `industry.banner` | industry | Industry interaction | `industry/industry-banner.jpg` | 1920 x 640 | 3:1 | Industry interaction session | placeholder |
| `hostel.hero` | hostel | Hostel facility | `hostel/hostel-hero.jpg` | 1600 x 900 | 16:9 | Hostel accommodation | placeholder |
| `hostel.room` | hostel | Hostel facility | `hostel/hostel-room.jpg` | 1200 x 800 | 3:2 | Hostel room interior | placeholder |
| `library.hero` | library | Library | `library/library-hero.jpg` | 1600 x 900 | 16:9 | College library | placeholder |
| `sports.hero` | sports | Sports | `sports/sports-hero.jpg` | 1600 x 900 | 16:9 | College sports ground | placeholder |
| `transport.hero` | transport | Transport facility | `transport/transport-hero.jpg` | 1600 x 900 | 16:9 | College bus fleet | placeholder |
| `canteen.hero` | canteen | Canteen | `canteen/canteen-hero.jpg` | 1600 x 900 | 16:9 | College canteen | placeholder |
| `cultural.hero` | cultural | Cultural activities | `cultural/cultural-hero.jpg` | 1600 x 900 | 16:9 | Cultural event on campus | placeholder |
| `student-zone.hero` | student-zone | Student zone | `student-zone/student-zone-hero.jpg` | 1600 x 900 | 16:9 | Students at SKEC | placeholder |
| `events.default-card` | events | News and events cards (fallback) | `events/event-default.jpg` | 1200 x 800 | 3:2 | College event | placeholder |
| `labs.hero` | labs | Laboratories and facilities | `labs/labs-hero.jpg` | 1600 x 900 | 16:9 | Laboratory facilities | placeholder |
| `gallery.cover` | gallery | Gallery landing page | `gallery/gallery-cover.jpg` | 1600 x 900 | 16:9 | Gallery cover | placeholder |
| `alumni.hero` | alumni | Alumni | `alumni/alumni-hero.jpg` | 1600 x 900 | 16:9 | SKEC alumni | placeholder |
| `committees.hero` | committees | Committees and grievance | `committees/committees-hero.jpg` | 1600 x 640 | 5:2 | College committees | placeholder |

Gallery photographs, event photographs and department staff portraits are **not** listed individually. They will be uploaded through the admin CMS in a later phase, each with its own alt text, credit and consent record.

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
