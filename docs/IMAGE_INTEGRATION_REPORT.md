# Image Integration Report

Source: `Skec.docx` (32 embedded images, mapped to labels through `word/document.xml` relationships; each label sits directly above its image) integrated into `SKEC-main.zip`.

**Verification levels used on the site**
- *Visible*: the photograph itself shows the SKEC name (signage, banner or caption).
- *Pending*: supplied by the project owner, plausible for the section, but nothing in the photo identifies the institution or department. Shown with a neutral description and the caption note "Supplied image, details pending confirmation" where captions appear.
- *Excluded*: contradicted by visible evidence, stock-style, or not matching the section. Kept in `assets/unused/`.

## 1. Extracted images and what they actually show

| # | Docx label | Format / size | Actual content | Level | Used |
|---|---|---|---|---|---|
| 1 | Skec-logo.svg, og-default.png | PNG 234x234 | Logo reading "Sri Krishna College of Engineering" with motto "Talent, Technique and Training" | Visible | Yes (header, footer) |
| 2 | dr-r-vivekanadhan.png | JPEG 581x538 | Portrait of a man at a desk (supplied as the Chairman's portrait) | Owner-supplied | Yes |
| 3 | home-hero.png | JPEG 1500x695 | Pink multi-storey block with "Sri Krishna Engineering College" on the roof | Visible | Yes |
| 4 | home-facility-library.png | JPEG 1200x670 | Students at a large table in a library | Pending | Yes |
| 5 | home-faciliy-transport.png | JPEG 900x500 | Rows of yellow buses in a yard | Pending | Yes |
| 6 | home-facility-hostel.png | JPEG 1200x798 | Room with beds, desks, wardrobe | Pending | Yes |
| 7 | campus-overview.png | JPEG 1280x963 | Entrance gate with "Sri Krishna Engineering College" board | Visible | Yes |
| 8 | vision-banner.png | JPEG 756x503 | Stage party at "Fusion 2.11 National Level Technical Symposium", SKEC logo, "2026" on banner | Visible | Yes (news) |
| 9 | (unlabelled, after #8) | JPEG 1600x737 | Admission-open flyer collage with statistics | Excluded | No |
| 10 | leadership-banner.png | PNG 1200x630 | Stock graduates, "Benefits of student leadership" | Excluded | No |
| 11 | campus-hero.png | JPEG 1200x801 | Orange/cream building, flag, palms | Excluded | No |
| 12 | infrastructure.png | JPEG 671x400 | Long orange building, lawn | Excluded | No |
| 13 | dept-cse.png | MPO 1100x500 | Staff group under Hindi "Uttar Pradesh / North Entry" CSE sign | Excluded | No |
| 14 | dept-ece.png | JPEG 1600x900 | ECE building entrance, no institution marking | Excluded | No |
| 15 | dept-eee.png | JPEG 768x404 | Students around electrical machines | Pending | Yes |
| 16 | dept-aids.png | PNG 474x290 | AI & Data Science signboard, other campus look | Excluded | No |
| 17 | dept-it.png | JPEG 533x400 | Students at computers | Pending | Yes |
| 18 | dept-ft.png | JPEG 1024x576 | Man at monitors, stock/AI style | Excluded | No |
| 19 | dept-mba.png | JPEG 612x372 | Lecture in tiered classroom | Pending | Yes |
| 20 | dept-me.png | PNG 474x257 | Students at lathes | Pending | Yes |
| 21 | admission-banner.png | PNG 474x474 | "Admissions 2025" graphic with phone numbers | Excluded | No |
| 22 | prospectus-cover.png | PNG 436x218 | Building sign reads "Sree Krishna College of Engineering, Anaicut, Vellore" | Excluded | No |
| 23 | placement-hero.png | JPEG 960x400 | Group photo captioned "Placements @ SKEC" | Visible | Yes |
| 24 | internships.png | JPEG 390x244 | Uniformed students with a book on a lawn | Excluded | No |
| 25 | hostal-hero.png | JPEG 683x512 | Bunk-bed room, commercial-hostel/stock look | Excluded | No |
| 26 | library-hero.png | PNG 474x245 | Library stacks | Pending | Yes |
| 27 | sports-hero.png | JPEG 670x500 | Outdoor volleyball match | Pending | Yes |
| 28 | cateen-hero.png | JPEG 1024x608 | Dining hall with students | Pending | Yes |
| 29 | labs-hero.png | JPEG 1075x716 | Computer lab, long bench | Pending | Yes |
| 30 | cultural-hero.png | JPEG 1280x720 | Stage group, banner "Aaravam '23" | Pending | Yes |
| 31 | student-zone-hero.png | JPEG 1280x720 | Students on steps, stock style | Excluded | No |
| 32 | alumini-hero.png | JPEG 1379x919 | Seminar audience, not alumni | Excluded | No |

No filename in the document swapped one facility for another (e.g. hostel/library were correctly labelled), but several labels did not match the photograph (#8 "vision-banner" is an event photo, #22 "prospectus-cover" is a different college, #32 "alumni" is a seminar).

## 2. Placement report

Final files are under `frontend/public/images/`. Every placed photograph is the original docx file, byte for byte (no re-encoding).

| Docx image | Final file | Where it appears | Reason |
|---|---|---|---|
| 1 | `brand/skec-logo.png` | Header, footer | Original raster used; the earlier traced SVG deviated from it |
| 2 | `chairman/dr-r-vivekanandhan.jpg` | `/founder-and-chairman` | Chairman portrait, unaltered (pixel-identical to the file already in the project) |
| 3 | `hero/skec-main-building-hero.jpg` | Home hero, `/about` | Shows the college name |
| 4 | `library/library-reading-hall.jpg` | Home facility card, `/library` | Library reading area |
| 5 | `transport/college-buses.jpg` | Home facility card, `/transport` | Transport |
| 6 | `hostel/hostel-room.jpg` | Home facility card, `/hostel` | Hostel |
| 7 | `about/main-entrance-gate.jpg` | Home "trusted starting point", `/about` | Shows the college name |
| 8 | `events/fusion-2-11-symposium-2026.jpg` | `/news-and-events` | Event banner names SKEC and the event |
| 15 | `departments/eee-electrical-machines-lab.jpg` | `/departments` | Electrical machines lab |
| 17 | `departments/it-computer-lab.jpg` | `/departments` | Computer lab |
| 19 | `departments/mba-lecture-hall.jpg` | `/departments` | Lecture hall |
| 20 | `departments/me-machine-workshop.png` | `/departments` | Machine workshop |
| 23 | `placements/placements-at-skec.jpg` | `/placements` | Caption names SKEC placements |
| 26 | `library/library-stacks.png` | `/library` hero | Library |
| 27 | `sports/volleyball-court.jpg` | `/sports` | Sports |
| 28 | `canteen/canteen-dining-hall.jpg` | `/infrastructure` | Canteen (no canteen page exists) |
| 29 | `labs/computer-laboratory.jpg` | `/infrastructure` hero | Laboratories (no labs page exists) |
| 30 | `cultural/aaravam-23-cultural-programme.jpg` | `/campus-life` hero | Cultural events (no cultural page exists) |

Notes: department photos sit on `/departments` because no per-department pages exist. Small originals (under 700 px wide) are capped near native size so they are not upscaled. Pages with no suitable verified photo keep the branded placeholder: `/admissions`, `/vision-and-mission`, `/administration`, `/alumni`, `/student-zone`.

## 3. Images not used
See `assets/unused/README.md` for each file and reason (14 photographs, plus the traced logo SVG).

## 4. Modified and added source files
Modified: `frontend/app/page.tsx`, `frontend/app/[slug]/page.tsx`, `frontend/app/globals.css`, `frontend/components/site.tsx`, `frontend/src/content/image-manifest.json`, `docs/ASSET_MANIFEST.md`, `assets/README.md`, `scripts/generate_asset_manifest.py` (now refuses to run without `--force`).
Added: `frontend/components/media.tsx` (manifest-driven `SiteImage`), `assets/unused/`, this report, 17 image files.
Removed (replaced by the originals above): `hero/campus-hero.png`, `library/library-hero.png`, `chairman/dr-r-vivekanadhan.png` (all pixel-identical re-encodes of docx images 3, 4, 2) and `brand/skec-logo.svg` (moved to `assets/unused/`).
Changed page copy: the Chairman, Infrastructure and News pages no longer say photos are missing; the home "Image-ready" block became a Campus facilities strip.

## 5. Verification actually run
- `npx tsc --noEmit`: no errors.
- `npx eslint .`: no output (clean).
- `npx vitest run`: 1 file, 2 tests passed.
- `npx next build`: succeeded, 35 static pages generated.
- Served the production build: 39 image requests across 18 pages, all HTTP 200 with image content types; no failures.
- Headless Chromium at 1440, 820 and 390 px on 6 pages (home, about, chairman, departments, library, infrastructure): no horizontal overflow; images loaded on repeat checks. I viewed the desktop home, desktop chairman and mobile departments screenshots; I did not visually review every page at every width.
- Backend: no backend files were changed, so backend tests were not run.
- `scripts/validate_phase0.py` was run and fails 8 of 29 checks. It is an outdated Phase 0 script (for example it asserts that no application code exists), so those failures are not caused by this work and I did not treat it as a gate.

## 6. Issues needing your decision
1. The logo reads "Sri Krishna College of Engineering", while the site, gate and roof signage say "Sri Krishna Engineering College". Confirm the correct institutional name.
2. The "pending" photographs carry no identifying marks. Confirm they are SKEC photographs and that department attributions are right before launch.
3. Image 8's month is partly cut off on the banner, so only the year 2026 is stated.
4. No 1200x630 social-sharing image was supplied, so `brand.og-image` is still a placeholder.

## 7. Run locally
```bash
cd frontend
npm install
npm run lint && npx tsc --noEmit && npm test
npm run build
npm run dev        # http://localhost:3000
```
Full stack: `docker compose up --build` from the project root (see `README.md`).
