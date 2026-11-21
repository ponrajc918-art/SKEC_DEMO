# Design System

Phase 0 deliverable. This is a **specification**; no UI has been built or visually tested yet. Phase 1 turns it into Tailwind tokens, shadcn/ui theme variables and components.

## 1. Design intent

A premium, calm, editorial engineering-college website: deep navy for authority, white and warm neutrals for space, champagne gold used sparingly as an accent. The reference feel is a well-edited international university site, not a template.

**Do:** generous whitespace, strong typographic hierarchy, restrained motion, consistent cards, real content before decoration.

**Avoid:** heavy gradients, neon colours, cartoon icons, random stock photography, crowded mega-sections, decorative effects that carry no meaning, and keyword-stuffed titles.

## 2. Colour tokens

| Token | Hex | Use |
|---|---|---|
| `navy-950` | `#07142A` | Footer, deepest surfaces |
| `navy-900` | `#0B1F3A` | Primary brand colour, headings, primary buttons |
| `navy-800` | `#12305A` | Hover state, secondary surfaces |
| `navy-700` | `#1B4276` | Links on light backgrounds, focus accents |
| `gold-500` | `#C8A96A` | Champagne gold accent on navy, rules, small ornaments |
| `gold-300` | `#E3D3A8` | Subtle highlights, tints |
| `gold-700` | `#7A5F2A` | Gold-toned **text** on light backgrounds |
| `sand-50` | `#F7F3EA` | Warm neutral page background (alternate sections) |
| `white` | `#FFFFFF` | Base background, cards |
| `slate-600` | `#4A5568` | Body secondary text |
| `danger-600` | `#B42318` | Errors |
| `success-600` | `#0F6B3A` | Success |
| `warning-700` | `#8A5A00` | Warnings |

Gold is an accent. Maximum one gold element per viewport region (a rule, an icon ring or a small badge). Large gold fills are not used.

### Contrast (computed with the WCAG 2.x relative-luminance formula)

| Foreground on background | Ratio | Verdict |
|---|---|---|
| navy-900 on white | 16.52:1 | AA and AAA, all text sizes |
| navy-900 on sand-50 | 14.92:1 | AA and AAA |
| white on navy-800 | 13.16:1 | AA and AAA |
| gold-500 on navy-900 | 7.35:1 | AA and AAA |
| navy-700 on white | 10.06:1 | AA and AAA |
| slate-600 on white | 7.53:1 | AA and AAA |
| slate-600 on sand-50 | 6.80:1 | AA and AAA |
| gold-700 on white | 6.00:1 | AA, body text allowed |
| gold-700 on sand-50 | 5.42:1 | AA, body text allowed |
| danger-600 on white | 6.57:1 | AA |
| success-600 on white | 6.59:1 | AA |
| warning-700 on white | 5.93:1 | AA |
| `#9A7B3F` (not a token) on white | 3.98:1 | **Fails AA for body text.** Do not use for text. |

Rule: never use gold-500 as text on white or sand. Use gold-700 for gold-toned text on light surfaces. These numbers were computed in Phase 0; they must be re-checked in a browser with real rendering in Phase 1.

## 3. Typography

| Role | Typeface | Notes |
|---|---|---|
| Headings, display | Source Serif 4 | Open font (SIL OFL). Editorial, serious tone. |
| Body, UI, forms, tables | Inter | Open font (SIL OFL). Highly legible at small sizes. |
| Tamil text (optional, later) | Noto Sans Tamil / Noto Serif Tamil | Reserved for bilingual content if the college requests it. |
| Code, IDs | system monospace | Admin portals only. |

Fonts are self-hosted through `next/font` so no third-party font request happens at page view. All typefaces are free and open source.

### Type scale (rem, 16px root)

| Style | Size / line height | Weight | Use |
|---|---|---|---|
| Display | 3.5 / 1.1 (desktop), 2.25 / 1.15 (mobile) | 600, serif | Home hero only |
| H1 | 2.5 / 1.15 (desktop), 2 / 1.2 (mobile) | 600, serif | Page titles |
| H2 | 1.875 / 1.25 | 600, serif | Section titles |
| H3 | 1.375 / 1.35 | 600, sans | Card titles, subsections |
| H4 | 1.125 / 1.4 | 600, sans | Minor headings |
| Body | 1 / 1.65 | 400, sans | Paragraphs (max line length about 70 characters) |
| Small | 0.875 / 1.5 | 400, sans | Captions, metadata |
| Overline | 0.75 / 1.4, uppercase, +0.08em tracking | 600, sans | Section eyebrow labels |

Minimum body size is 16px. Numbers in tables use tabular figures.

## 4. Spacing, layout and radius

- Base unit **4px**; use the Tailwind spacing scale (4, 8, 12, 16, 24, 32, 48, 64, 96, 128).
- Section vertical rhythm: 64px on mobile, 96px on tablet, 128px on desktop.
- Container: max width 1280px, side padding 16px (mobile), 32px (tablet), 48px (desktop). Reading column for long text: max 720px.
- 12-column grid at `lg` and above, 4 columns on mobile, 8 on tablet.
- Radius: 6px inputs and buttons, 12px cards, 9999px badges. No heavy drop shadows; use a 1px border `slate-200` and a soft `shadow-sm`, with `shadow-md` on hover only.

## 5. Responsive breakpoints

| Name | Min width | Typical behaviour |
|---|---|---|
| base | 0 | Single column, drawer navigation |
| `sm` | 640px | Two-column card grids start |
| `md` | 768px | Tablet layouts, side-by-side media and text |
| `lg` | 1024px | Desktop navigation, 3-column grids |
| `xl` | 1280px | Full container width |
| `2xl` | 1536px | Container stays at 1280px; larger hero imagery only |

Mobile first. Every page must work from 320px width without horizontal scrolling. The majority of prospective students and parents browse on phones, so mobile is the primary design target.

## 6. Components

### Buttons

| Variant | Appearance | Use |
|---|---|---|
| Primary | navy-900 fill, white text, navy-800 hover | Main action per section ("Apply now") |
| Secondary | white fill, navy-900 text, 1px navy-900 border | Alternative action |
| Accent | gold-500 fill, navy-900 text | At most once per page, for the admissions call to action |
| Ghost | no fill, navy-700 text, underline on hover | Tertiary and inline actions |
| Destructive | danger-600 fill, white text | Portals only |

Sizes: 40px (default), 48px (large), 32px (compact, portals). Minimum touch target 44 x 44px. A visible 2px focus ring in navy-700 with a 2px white offset (gold-500 ring on navy backgrounds). Loading and disabled states are specified for every variant.

### Cards

| Card | Contents |
|---|---|
| Content card | Image (16:9 or 3:2), eyebrow, H3, two-line summary, text link |
| Programme card | Degree badge, programme name, short descriptor, link to detail |
| Person card | Portrait (4:5), name, designation, qualification line |
| Event/news card | Date badge, title, category, link |
| Stat card | Large figure, label, source and "as of" date (only for verified figures) |
| Notice card | Date, title, download link with file type and size |

Cards are white with a 1px border and 12px radius; whole card is one focusable link target where appropriate.

### Navigation

- **Utility bar** (top, navy-950): admission-open notice, phone, email, "Student Login", "Staff Login" (links only after portals exist).
- **Main bar:** logo left, primary navigation right, "Apply" accent button.
- **Primary IA (mirrors the official site, simplified):** About, Academics, Admissions, Placements, Campus Life, News and Events, Committees, Contact.
- **Desktop:** mega-menu panels with grouped links (focus-trap free, keyboard operable with arrow keys and Escape).
- **Mobile:** full-height drawer with accordion groups, large tap targets, search field.
- **Breadcrumbs** on all pages below depth 1. **Skip to content** link is the first focusable element.
- **Footer:** quick links, contact block (address and phones only after verification), mandatory-disclosure links, social links, accreditation notices (only verified).

### Forms

Visible labels, helper text below the field, inline error text with an icon (not colour alone), error summary at the top for long forms, server-side validation mirrored client-side, honeypot plus rate limiting on public enquiry forms.

### Tables (portals)

Sticky header, sortable columns, row actions in a trailing menu, mobile layout collapses to labelled cards, bulk actions require confirmation.

## 7. Image placeholders

The site must never show an empty grey box or a fake photograph.

**`SiteImage` component contract (Phase 1):**

```text
<SiteImage id="home.hero" />   // looks up id in image-manifest.json
status === "approved"  -> renders the real image (next/image, correct alt, dimensions, priority flag for hero)
otherwise              -> renders <ImagePlaceholder category="hero" ratio="16:9" />
```

**Placeholder visual treatment (CSS only, no raster art):**

- Flat navy-900 or sand-50 surface with a 1px gold-500 inner frame inset 12px.
- A thin line-art category glyph from Lucide (building, book-open, bed, trophy, bus, flask-conical, graduation-cap, users) centred at 25% opacity.
- A small SKEC monogram in a corner (SVG drawn from the official logo once supplied; a plain typographic "SKEC" until then).
- Optional caption "Official photograph to be added", shown only when `NEXT_PUBLIC_SHOW_PLACEHOLDER_LABELS=true`, so production never advertises a missing image.
- Aspect ratio is reserved with `aspect-ratio` so replacing the placeholder causes no layout shift.
- Placeholders are `aria-hidden` and carry no alt text, so screen readers hear nothing misleading.

**Chairman portrait slot:** a 4:5 frame with the same treatment plus the verified name and designation caption beside it. The portrait is only the genuine supplied photograph, and no placeholder ever depicts a face or silhouette that could be mistaken for him.

## 8. Layout patterns

| Pattern | Description |
|---|---|
| Home hero | Full-width image slot with navy overlay at the bottom third, display heading, one primary and one secondary button, admissions notice strip below |
| Page header | Eyebrow, H1, one-sentence intro, breadcrumb; optional banner slot (3:1) |
| Two-column feature | Text and image, alternating sides, 7/5 split at `lg` |
| Card grid | 1 / 2 / 3 / 4 columns by breakpoint, equal-height cards |
| Programme directory | Filter by level (UG/PG), then card grid |
| Detail page | Left sticky in-page nav on desktop, content column up to 720px, right rail for contacts and downloads |
| Timeline | Vertical timeline for history, with the verification badge from CONTENT_VERIFICATION.md on each milestone until confirmed |
| Document list | Table of circulars/downloads with date, title, file type, size, download button |
| Portal shell | Left sidebar by role, top bar with search and notifications, content area, consistent page headers and tables |

## 9. Motion

Subtle only: 150 to 250ms fades and 8px translations on scroll-in, hover elevation on cards, accordion height transitions. All motion is disabled under `prefers-reduced-motion: reduce`. No parallax, auto-playing carousels or looping animations.

## 10. Accessibility principles

Target **WCAG 2.2 level AA**.

- Semantic HTML landmarks (`header`, `nav`, `main`, `footer`), one H1 per page, no skipped heading levels.
- Full keyboard operation with visible focus; no keyboard traps; logical tab order.
- Colour is never the sole signal; contrast per the table above.
- Text resizable to 200% without loss of content; `rem` units; no fixed-height text containers.
- Touch targets at least 44 x 44px.
- Alt text per the manifest policy; decorative images hidden from assistive technology.
- Form labels, error identification and instructions programmatically associated.
- Links have meaningful text (no bare "click here"); PDFs are labelled with type and size.
- `lang="en"` on the document; `lang="ta"` on any Tamil passages.
- Automated checks (axe via Playwright) run in CI from Phase 1; manual screen-reader and keyboard review is listed in the Phase 6 acceptance criteria. None of this has been executed yet.

## 11. Tooling decisions

Tailwind CSS tokens defined in `tailwind.config` from the table above; shadcn/ui components copied into the repository and restyled to these tokens (so the college owns the code); Lucide for icons (outline style, 1.5px stroke). A `design-tokens.md` is not kept separately; this file is authoritative and the Tailwind config must match it.
