#!/usr/bin/env python3
"""Validate the Phase 0 deliverables. Run from anywhere: python3 scripts/validate_phase0.py
Exit code 0 means every check passed. Output lists each check honestly."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


REQUIRED = [
    "README.md", "docs/ARCHITECTURE.md", "docs/DESIGN_SYSTEM.md", "docs/PAGE_INVENTORY.md",
    "docs/ASSET_MANIFEST.md", "docs/CONTENT_VERIFICATION.md", "docs/DATABASE_PLAN.md",
    "docs/PROJECT_PROGRESS.md", "docs/PRODUCTION_COSTS.md", "docs/PHASE_ROADMAP.md",
    ".env.example", ".gitignore",
]

# 1. Required files exist and are non-trivial
missing = [f for f in REQUIRED if not (ROOT / f).is_file()]
check("All 12 required files exist", not missing, f"missing: {missing}" if missing else "")
tiny = [f for f in REQUIRED if (ROOT / f).is_file() and (ROOT / f).stat().st_size < 400]
check("No required file is trivially small", not tiny, f"small: {tiny}" if tiny else "")

# 2. Markdown documents start with an H1
md_files = [f for f in REQUIRED if f.endswith(".md") and (ROOT / f).is_file()]
bad_h1 = [f for f in md_files if not (ROOT / f).read_text(encoding="utf-8").lstrip().startswith("# ")]
check("Every required Markdown file starts with a level-1 heading", not bad_h1, str(bad_h1) if bad_h1 else "")

# 3. All seven phases are documented consistently
phase_docs = ["README.md", "docs/PROJECT_PROGRESS.md", "docs/PHASE_ROADMAP.md"]
for f in phase_docs:
    t = (ROOT / f).read_text(encoding="utf-8")
    absent = [n for n in range(7) if not re.search(rf"\bPhase {n}\b|\| {n} \|", t)]
    check(f"{f} names Phases 0-6", not absent, f"absent: {absent}" if absent else "")
rt = (ROOT / "docs/PHASE_ROADMAP.md").read_text(encoding="utf-8")
heads = re.findall(r"^## Phase (\d):", rt, flags=re.M)
check("PHASE_ROADMAP has a section for each of Phases 0-6", heads == [str(i) for i in range(7)], f"found {heads}")
check("PHASE_ROADMAP has acceptance criteria for each phase",
      len(re.findall(r"\*\*Acceptance criteria\*\*", rt)) == 7,
      f"count={len(re.findall(r'Acceptance criteria', rt))}")

# 4. Relative Markdown links resolve
broken = []
for f in md_files:
    base = (ROOT / f).parent
    for target in re.findall(r"\]\(([^)\s]+)\)", (ROOT / f).read_text(encoding="utf-8")):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        p = (base / target.split("#")[0]).resolve()
        if not p.exists():
            broken.append(f"{f} -> {target}")
check("All relative Markdown links resolve", not broken, "; ".join(broken))

# 5. Image manifest consistency (JSON vs Markdown vs folders)
mj = json.loads((ROOT / "frontend/src/content/image-manifest.json").read_text(encoding="utf-8"))
ids_json = [i["id"] for i in mj["images"]]
md = (ROOT / "docs/ASSET_MANIFEST.md").read_text(encoding="utf-8")
ids_md = re.findall(r"^\| `([a-z0-9\-]+\.[a-z0-9\-]+)` \|", md, flags=re.M)
check("Manifest JSON and Markdown list the same IDs in the same order", ids_json == ids_md,
      f"json={len(ids_json)} md={len(ids_md)}")
check("Manifest IDs are unique", len(ids_json) == len(set(ids_json)))
allowed = {"placeholder", "awaiting-user-supplied", "awaiting-official", "approved"}
check("Manifest statuses use the defined vocabulary", all(i["status"] in allowed for i in mj["images"]))
check("No manifest slot is marked approved in Phase 0", not any(i["status"] == "approved" for i in mj["images"]))
no_dir = sorted({i["category"] for i in mj["images"] if not (ROOT / "frontend/public/images" / i["category"]).is_dir()})
check("Every manifest category has an image folder", not no_dir, str(no_dir) if no_dir else "")
required_fields = {"id", "category", "page", "path", "width", "height", "aspectRatio", "alt", "status"}
check("Every manifest entry has all required fields", all(required_fields <= set(i) for i in mj["images"]))
check("Chairman portrait slot exists and awaits the user-supplied file",
      any(i["id"] == "chairman.portrait" and i["status"] == "awaiting-user-supplied" for i in mj["images"]))
real_imgs = [p.name for p in (ROOT / "frontend/public/images").rglob("*")
             if p.is_file() and p.name != ".gitkeep"]
check("No image files are bundled (placeholders only)", not real_imgs, str(real_imgs) if real_imgs else "")

# 6. .env.example holds placeholders only
env_lines = (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
sensitive_key = re.compile(r"(SECRET|PASSWORD|ACCESS_KEY|KEY_ID|ENCRYPTION_KEY|DSN|USERNAME)$|^DATABASE_URL$", re.I)
offenders = []
for ln in env_lines:
    if ln.strip().startswith("#") or "=" not in ln:
        continue
    k, v = ln.split("=", 1)
    v = v.split("#")[0].strip()
    if sensitive_key.search(k.strip()) and v and "__" not in v:
        offenders.append(k.strip())
check(".env.example sensitive keys are empty or __PLACEHOLDER__ only", not offenders, str(offenders))
check(".env.example sets PAYMENT_MODE=test", any(l.startswith("PAYMENT_MODE=test") for l in env_lines))

# 7. Secret-pattern scan across every text file
patterns = {
    "AWS access key": r"AKIA[0-9A-Z]{16}",
    "Razorpay key": r"rzp_(live|test)_[A-Za-z0-9]{8,}",
    "Private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "OpenAI/Anthropic-style key": r"\bsk-[A-Za-z0-9_\-]{20,}",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    "Slack token": r"\bxox[abprs]-[A-Za-z0-9\-]{10,}",
    "Password in URL": r"://[^\s:/@]+:(?!__)[^\s@/]{4,}@",
}
hits = []
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".md", ".json", ".py", ".txt", ".example", ""} or p.name in {".env.example", ".gitignore"}:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for label, pat in patterns.items():
            if re.search(pat, text):
                hits.append(f"{p.relative_to(ROOT)}: {label}")
check("No secret-like strings found in any text file", not hits, "; ".join(hits))
check("No .env file is present", not list(ROOT.glob(".env")) and not list(ROOT.rglob(".env.local")))

# 8. Honest scope: no application code is claimed or present
app_code = [str(p.relative_to(ROOT)) for p in list(ROOT.glob("backend/**/*.py")) + list(ROOT.glob("frontend/**/package.json"))
            + list(ROOT.glob("frontend/**/*.tsx"))]
check("No application code present (Phase 0 is documentation and skeleton only)", not app_code, str(app_code))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
check("README states that nothing is implemented yet", "No website or ERP has been implemented yet" in readme)

# 9. Cross-document consistency on key facts
ct = (ROOT / "docs/CONTENT_VERIFICATION.md").read_text(encoding="utf-8")
inv = (ROOT / "docs/PAGE_INVENTORY.md").read_text(encoding="utf-8")
arch = (ROOT / "docs/ARCHITECTURE.md").read_text(encoding="utf-8")
db = (ROOT / "docs/DATABASE_PLAN.md").read_text(encoding="utf-8")
check("Argon2id is stated in ARCHITECTURE and .env/progress consistently",
      "Argon2id" in arch and "ARGON2_" in (ROOT / ".env.example").read_text(encoding="utf-8"))
check("Razorpay test-mode-first appears in ARCHITECTURE, ROADMAP and COSTS",
      all("test mode" in (ROOT / f).read_text(encoding="utf-8").lower() for f in
          ["docs/ARCHITECTURE.md", "docs/PHASE_ROADMAP.md", "docs/PRODUCTION_COSTS.md"]))
check("User-supplied history H-01..H-05 recorded", all(f"H-0{i}" in ct for i in range(1, 6)))
check("Chairman name recorded consistently", all("Vivekanandhan" in t for t in (ct, inv)))
check("Page inventory numbering 1..42 is complete",
      [int(n) for n in re.findall(r"^\| (\d+) \| `/", inv, flags=re.M)] == list(range(1, 43)),
      f"found {len(re.findall(r'^\| (\d+) \| `/', inv, flags=re.M))}")
check("Database plan names the Razorpay idempotency key and gap-free receipts",
      "idempotency_key" in db and "gap-free" in db)

width = max(len(n) for n, _, _ in results)
failed = 0
for name, ok, detail in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -> {detail}" if (detail and not ok) else ""))
    failed += 0 if ok else 1
print(f"\n{len(results) - failed} passed, {failed} failed, {len(results)} total")
sys.exit(1 if failed else 0)
