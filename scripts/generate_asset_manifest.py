#!/usr/bin/env python3
"""Generate docs/ASSET_MANIFEST.md and frontend/src/content/image-manifest.json.

Single source of truth for image slots: the SLOTS list below. Re-run after editing:
    python3 scripts/generate_asset_manifest.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (id, category, page, filename, width, height, ratio, alt, status_note)
# Status values: placeholder | awaiting-user-supplied | awaiting-official | approved
CH = "awaiting-user-supplied"
PH = "placeholder"
SLOTS = [
    ("brand.logo", "brand", "Header, footer, favicon source", "brand/skec-logo.svg", 512, 512, "1:1",
     "Sri Krishna Engineering College logo", "awaiting-official"),
    ("brand.og-image", "brand", "Social sharing preview (all pages)", "brand/og-default.jpg", 1200, 630, "1.91:1",
     "Sri Krishna Engineering College", PH),
    ("chairman.portrait", "chairman", "Founder Chairman page, home welcome block", "chairman/dr-r-vivekanandhan.jpg", 800, 1000, "4:5",
     "Portrait of Dr. R. Vivekanandhan, Founder Chairman, Sri Krishna Educational Trust", CH),
    ("home.hero", "hero", "Home hero", "hero/home-hero.jpg", 1920, 1080, "16:9",
     "Sri Krishna Engineering College campus", PH),
    ("home.facility-library", "hero", "Home facilities strip", "hero/home-facility-library.jpg", 1200, 800, "3:2",
     "College library reading area", PH),
    ("home.facility-transport", "hero", "Home facilities strip", "hero/home-facility-transport.jpg", 1200, 800, "3:2",
     "College transport buses", PH),
    ("home.facility-hostel", "hero", "Home facilities strip", "hero/home-facility-hostel.jpg", 1200, 800, "3:2",
     "College hostel building", PH),
    ("about.campus-overview", "about", "About the college", "about/campus-overview.jpg", 1600, 900, "16:9",
     "Aerial or wide view of the SKEC campus", PH),
    ("about.vision-banner", "about", "Vision and mission", "about/vision-banner.jpg", 1920, 640, "3:1",
     "Students on campus", PH),
    ("about.leadership-banner", "about", "Leadership and administration", "about/leadership-banner.jpg", 1920, 640, "3:1",
     "College administrative block", PH),
    ("campus.hero", "campus", "Our campus", "campus/campus-hero.jpg", 1920, 800, "12:5",
     "Main campus view", PH),
    ("campus.infrastructure", "campus", "Infrastructure", "campus/infrastructure.jpg", 1600, 900, "16:9",
     "Academic block and grounds", PH),
    ("dept.cse", "departments", "Department: B.E. Computer Science and Engineering", "departments/dept-cse.jpg", 1600, 900, "16:9",
     "Computer Science and Engineering department", PH),
    ("dept.ece", "departments", "Department: B.E. Electronics and Communication Engineering", "departments/dept-ece.jpg", 1600, 900, "16:9",
     "Electronics and Communication Engineering department", PH),
    ("dept.eee", "departments", "Department: B.E. Electrical and Electronics Engineering", "departments/dept-eee.jpg", 1600, 900, "16:9",
     "Electrical and Electronics Engineering department", PH),
    ("dept.aids", "departments", "Department: B.Tech. Artificial Intelligence and Data Science", "departments/dept-aids.jpg", 1600, 900, "16:9",
     "Artificial Intelligence and Data Science department", PH),
    ("dept.it", "departments", "Department: B.Tech. Information Technology", "departments/dept-it.jpg", 1600, 900, "16:9",
     "Information Technology department", PH),
    ("dept.ft", "departments", "Department: B.Tech. Fashion Technology", "departments/dept-ft.jpg", 1600, 900, "16:9",
     "Fashion Technology department", PH),
    ("dept.mba", "departments", "Department: M.B.A.", "departments/dept-mba.jpg", 1600, 900, "16:9",
     "Management Studies department", PH),
    ("dept.me", "departments", "PG programmes: M.E. (Applied Electronics, Computer Science)", "departments/dept-me.jpg", 1600, 900, "16:9",
     "Postgraduate engineering programmes", PH),
    ("admissions.banner", "admissions", "Admissions, UG, PG", "admissions/admissions-banner.jpg", 1920, 640, "3:1",
     "Admissions at SKEC", PH),
    ("admissions.prospectus-cover", "admissions", "Prospectus", "admissions/prospectus-cover.jpg", 900, 1200, "3:4",
     "Prospectus cover", "awaiting-official"),
    ("placements.hero", "placements", "Placements and recruitments", "placements/placements-hero.jpg", 1920, 800, "12:5",
     "Training and Placement Cell activity", PH),
    ("placements.internships", "placements", "Internships", "placements/internships.jpg", 1600, 900, "16:9",
     "Student internship activity", PH),
    ("industry.banner", "industry", "Industry interaction", "industry/industry-banner.jpg", 1920, 640, "3:1",
     "Industry interaction session", PH),
    ("hostel.hero", "hostel", "Hostel facility", "hostel/hostel-hero.jpg", 1600, 900, "16:9",
     "Hostel accommodation", PH),
    ("hostel.room", "hostel", "Hostel facility", "hostel/hostel-room.jpg", 1200, 800, "3:2",
     "Hostel room interior", PH),
    ("library.hero", "library", "Library", "library/library-hero.jpg", 1600, 900, "16:9",
     "College library", PH),
    ("sports.hero", "sports", "Sports", "sports/sports-hero.jpg", 1600, 900, "16:9",
     "College sports ground", PH),
    ("transport.hero", "transport", "Transport facility", "transport/transport-hero.jpg", 1600, 900, "16:9",
     "College bus fleet", PH),
    ("canteen.hero", "canteen", "Canteen", "canteen/canteen-hero.jpg", 1600, 900, "16:9",
     "College canteen", PH),
    ("cultural.hero", "cultural", "Cultural activities", "cultural/cultural-hero.jpg", 1600, 900, "16:9",
     "Cultural event on campus", PH),
    ("student-zone.hero", "student-zone", "Student zone", "student-zone/student-zone-hero.jpg", 1600, 900, "16:9",
     "Students at SKEC", PH),
    ("events.default-card", "events", "News and events cards (fallback)", "events/event-default.jpg", 1200, 800, "3:2",
     "College event", PH),
    ("labs.hero", "labs", "Laboratories and facilities", "labs/labs-hero.jpg", 1600, 900, "16:9",
     "Laboratory facilities", PH),
    ("gallery.cover", "gallery", "Gallery landing page", "gallery/gallery-cover.jpg", 1600, 900, "16:9",
     "Gallery cover", PH),
    ("alumni.hero", "alumni", "Alumni", "alumni/alumni-hero.jpg", 1600, 900, "16:9",
     "SKEC alumni", PH),
    ("committees.hero", "committees", "Committees and grievance", "committees/committees-hero.jpg", 1600, 640, "5:2",
     "College committees", PH),
]

REPLACEMENT_STEPS = """\
1. Receive the official photograph and confirm in writing that the college approves its publication.
2. Place the untouched original in `assets/incoming/` (this folder is git-ignored apart from `.gitkeep`).
3. Crop to the aspect ratio in the table, export at the stated dimensions (and a 2x variant if needed) as JPEG or WebP, and save it to the exact path in the **Filename** column under `frontend/public/images/`.
4. Edit the matching entry in `frontend/src/content/image-manifest.json`: set `"status": "approved"`, add `"credit"` and `"approvedBy"`, and refine `"alt"` to describe the real photograph.
5. Re-run `python3 scripts/generate_asset_manifest.py` only if slots were added or removed; otherwise update this table's Status cell to match the JSON.
6. No page code changes are required: pages reference images by **ID** (for example `home.hero`), never by path. The `SiteImage` component (Phase 1) shows the branded placeholder until the status is `approved`.
"""


def build():
    entries = []
    for (sid, cat, page, fn, w, h, ratio, alt, status) in SLOTS:
        entries.append({
            "id": sid, "category": cat, "page": page,
            "path": f"/images/{fn}", "width": w, "height": h,
            "aspectRatio": ratio, "alt": alt, "status": status,
        })
    out_json = {
        "version": 1,
        "note": "Pages reference images by id. Status other than 'approved' renders a branded placeholder.",
        "images": entries,
    }
    (ROOT / "frontend/src/content/image-manifest.json").write_text(
        json.dumps(out_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Image Asset Manifest",
        "",
        "Phase 0 deliverable. Status: **no real photographs are included**. Every slot below is a placeholder or is awaiting a supplied file.",
        "",
        "The machine-readable twin of this table is `frontend/src/content/image-manifest.json`. Both are generated from `scripts/generate_asset_manifest.py` so they cannot drift apart.",
        "",
        "## Rules",
        "",
        "- Image collection is **not** a blocker for development. Slots render branded placeholders until a file is approved.",
        "- No fabricated photographs, stock photos or AI-generated images pretending to be SKEC buildings, students, staff or events.",
        "- The Founder Chairman portrait must be the genuine photograph supplied by the project owner. It is never generated, retouched beyond standard crop/exposure, or substituted.",
        "- Pages reference images by **ID**, so replacing a file never requires editing a page.",
        "",
        "## Status vocabulary",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| `placeholder` | Branded CSS placeholder is shown. Official photograph not yet supplied. |",
        "| `awaiting-user-supplied` | Needs a specific file that the project owner holds (Chairman portrait). |",
        "| `awaiting-official` | Needs an official college asset (logo master, prospectus cover). |",
        "| `approved` | Official, rights-cleared photograph is in place and approved by the college. |",
        "",
        "## Folder structure",
        "",
        "```text",
        "frontend/public/images/<category>/   served files (final, optimised)",
        "frontend/src/content/image-manifest.json   registry used by pages",
        "assets/incoming/                     untouched originals as received (not committed)",
        "assets/placeholders/                 source artwork for branded placeholders (Phase 1)",
        "```",
        "",
        f"## Image slots ({len(entries)})",
        "",
        "| ID | Category | Intended page | Filename (under `frontend/public/images/`) | Dimensions (px) | Aspect | Alt text (draft) | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for e in entries:
        fn = e["path"].replace("/images/", "")
        lines.append(f"| `{e['id']}` | {e['category']} | {e['page']} | `{fn}` | {e['width']} x {e['height']} | {e['aspectRatio']} | {e['alt']} | {e['status']} |")
    lines += [
        "",
        "Gallery photographs, event photographs and department staff portraits are **not** listed individually. They will be uploaded through the admin CMS in a later phase, each with its own alt text, credit and consent record.",
        "",
        "## Replacement instructions",
        "",
        REPLACEMENT_STEPS,
        "## Alt text policy",
        "",
        "- Describe what is visible, in one sentence, without keyword stuffing (the current official site stuffs alt text and page titles with search keywords; the new site must not).",
        "- Decorative images use empty alt text.",
        "- People are named only with their consent and verified identity.",
        "",
        "## Consent and rights checklist (before status becomes `approved`)",
        "",
        "- [ ] College approval recorded",
        "- [ ] Photographer or source credit recorded",
        "- [ ] Consent obtained where identifiable students (especially minors) or staff appear",
        "- [ ] Image free of watermarks from third-party stock libraries",
        "",
    ]
    (ROOT / "docs/ASSET_MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {len(entries)} slots")


if __name__ == "__main__":
    build()
