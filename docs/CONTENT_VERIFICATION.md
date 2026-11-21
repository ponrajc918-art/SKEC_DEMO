# Content Verification Register

Phase 0 deliverable. Research date: **2026-11-13**. Method: public pages and public PDFs of https://skec.edu.in/ fetched read-only from the Claude chat environment; https://online.skec.edu.in/ fetched once at its public root URL. No login was attempted, no restricted endpoint was touched, nothing on the existing systems was modified.

## 1. Status vocabulary

| Label | Meaning |
|---|---|
| **VERIFIED-SITE** | Read on the official site on the research date. Still needs college sign-off before it is published as final copy. |
| **USER-SUPPLIED** | Given by the project owner. Not yet confirmed by the institution. |
| **CONFLICT** | Two official sources disagree. Must be resolved by the college. |
| **OUTDATED** | Official source contains content that is clearly stale. Do not republish. |
| **MISSING** | Page or content exists but holds no usable information. |
| **UNAVAILABLE** | Could not be fetched or could not be read. |
| **NOT-INSPECTED** | Linked from navigation but not fetched in this session. Must be inspected before Phase 1 content is written. |
| **PLACEHOLDER** | Invented demo text. Allowed only in dev builds and always marked. |

No institutional fact may reach the production site while it is anything other than "approved by the college".

## 2. Pages inspected

| # | Official URL | Result | Notes |
|---|---|---|---|
| 1 | `/` (home) | Fetched | Navigation, facilities teasers, event cards, contact footer |
| 2 | `/Aboutus` | Fetched | History text, chairman name, advisor mention |
| 3 | `/Vision` | Fetched | Trust vision and mission |
| 4 | `/Founder` | Fetched | Chairman profile and message |
| 5 | `/Administration` | Fetched | Contains the objects of the Trust only; no leadership roster |
| 6 | `/Department` | Fetched | List of UG and PG programmes |
| 7 | `/UnderGraduate` | Fetched | Programme vision/mission, eligibility, how to apply, lateral entry |
| 8 | `/PostGraduate` | Fetched | PG programme vision/mission, eligibility |
| 9 | `/Prospectus` | Fetched | Page holds two images only; not machine-readable text |
| 10 | `/Contact` | Fetched | Address, phones, emails |
| 11 | `/Examination` | Fetched | Timetable list entries only |
| 12 | `/Circular` | Fetched | No circulars (see V-07) |
| 13 | `/Curriculum` | Fetched | Regulation-2025 syllabus PDF links |
| 14 | `/Recruitments` | Fetched | Training and Placement Cell description |
| 15 | `/assets/doc/Mandatory Disclosure.pdf` | Fetched, 53 pages | Text extracted; see V-09 |
| 16 | `online.skec.edu.in` (root only) | Fetched | See V-11 |

### Linked pages NOT inspected in this session

`/Admissions`, `/Academic` (regulations), `/Internships`, `/Industry`, `/Infrastructure`, `/Ourcampus`, `/Cultural`, `/Library`, `/Hostel`, `/Sports`, `/Transport`, `/Student`, `/Events`, `/Gallery`, `/Alumni`, `/Selfies`, `/Grivance`, `/Enquiry`, and the PDFs "AICTE EOA 2025-26", the faculty photo-list PDF, the prospectus images, the exam timetable PDFs and the syllabus PDFs.

Status: **NOT-INSPECTED**. For these pages only the one-line teaser text on the home page was read (library, transport, hostel, events, placements, infrastructure, campus life). Phase 1 begins with a content sweep of these pages (see PHASE_ROADMAP.md). Nothing in this register should be read as covering them.

## 3. Verified facts (VERIFIED-SITE, pending college sign-off)

| ID | Fact | Source |
|---|---|---|
| F-01 | Name: Sri Krishna Engineering College | all pages |
| F-02 | Address: Panapakkam, Near Padappai, Via Tambaram, Chennai - 601 301 | footer, `/Contact` |
| F-03 | Phones: +91 81108 61000 and +91 81108 62000 | footer, `/Contact` |
| F-04 | Counselling code: 1427 | header strip |
| F-05 | Programmes are described as approved by AICTE and affiliated to Anna University | `/UnderGraduate`, `/PostGraduate` |
| F-06 | Home banner announces "Admission open 2026-2027" for B.E/B.Tech, M.E and M.B.A | home |
| F-07 | Seat blocking amount stated as Rs. 10,000; no entrance examination for direct admission | `/UnderGraduate`, `/PostGraduate` |
| F-08 | Trust vision (three points) and mission (two points) as published | `/Vision` |
| F-09 | Public social links: YouTube, Facebook, X (Twitter), Instagram | footer |
| F-10 | Transport teaser: buses reach campus before 8.05 am on working days and leave at 3.40 pm | home |
| F-11 | Hostel teaser: separate hostels for boys and girls | home |
| F-12 | UG programmes listed on `/Department` and `/UnderGraduate`: B.E. CSE, B.E. ECE, B.E. EEE, B.Tech. AI and Data Science, B.Tech. Information Technology, B.Tech. Fashion Technology | `/Department`, `/UnderGraduate`, `/Curriculum` |

## 4. User-supplied institutional history (USER-SUPPLIED)

| ID | Claim from the project owner | Corroboration on official site | Status |
|---|---|---|---|
| H-01 | Sri Krishna Educational Trust established in **1999** | `/Aboutus` states 1999 | Matches site. Needs institutional confirmation. |
| H-02 | Sri Krishna Engineering College established in **2000** | `/Aboutus` states 2000 | Matches site. Needs institutional confirmation. |
| H-03 | Development of UG and PG programmes | `/Aboutus` gives ME-CSE 2007, ME-Applied Electronics and MBA 2008 | Details differ in count, see C-01. |
| H-04 | Sri Krishna Institute of Technology established in **2009** | `/Aboutus` states 2009 with "4 Core UG courses" | Matches site. Relationship of SKIT to SKEC (separate institution?) needs confirmation. |
| H-05 | Advisor **Prof. Dr. P. Ananthakrishnan** joined in **2002** | `/Aboutus` states "since 2002" | Matches site. Needs institutional confirmation. |

These are recorded exactly as supplied. No figure has been changed. The official page's "22 years of excellence" phrasing is stale (it implies about 2024) and must not be copied; compute any "years" figure from a confirmed founding year at build time or avoid it.

## 5. Conflicts (CONFLICT)

| ID | Conflict | Sources | Action needed from the college |
|---|---|---|---|
| C-01 | **Number of programmes.** About page: "5 UG and 3 PG courses", "9 UG Departments and 3 PG Courses" in total. `/Department` lists **6 UG and 4 PG** (adds B.Tech. AI and DS and M.E. AI and DS). `/PostGraduate` and `/Curriculum` list only **3 PG** (no M.E. AI and DS). The Mandatory Disclosure PDF lists 5 UG and 3 PG, with no AI and DS. | `/Aboutus`, `/Department`, `/PostGraduate`, `/Curriculum`, PDF | Supply the AICTE-approved programme list with intake. Confirm whether B.Tech. AI and DS and M.E. AI and DS are approved and admitting. |
| C-02 | **Contact email.** Footer on most pages: `skec4120@gmail.com`; `/Contact` page: `skec1427@gmail.com`; principal address `principal.skec@gmail.com` on every page; the PDF lists a different, older address. | footer vs `/Contact` vs PDF | Confirm official addresses. Recommend role-based addresses on the college domain. |
| C-03 | **Founder Chairman (Dr. R. Vivekanandhan) qualifications.** About page heading and footer: M.Sc., M.Ed., M.Phil., MBA., LLM, Ph.D. (matches the owner's text). `/Founder` page lists a much longer set including M.Tech (CSE), LLB, M.A. subjects and further M.Sc. degrees. The PDF's governance table lists only "Master of Education". | `/Aboutus`, `/Founder`, PDF | The college must supply the approved wording. Until then, the site uses the owner-supplied line only. |
| C-04 | **Regulations on Examination vs Curriculum.** `/Examination` lists timetables for 2021 and 2017 regulations; `/Curriculum` shows Regulation-2025 syllabi. | `/Examination`, `/Curriculum` | Confirm which regulations are current for each batch. |
| C-05 | **Institution naming.** The map embed is titled "Sri Krishna Institute Of Technology"; `/Recruitments` text refers to students of "SIT"; the PDF writes "SRIKRISHNA ENGINEERING COLLEGE" and "Srikrishna Educational Trust". | `/Contact`, `/Recruitments`, PDF | Confirm official spellings (Sri Krishna vs Srikrishna) and whether SKIT shares this campus or website. |

## 6. Outdated, missing and stale content

| ID | Finding | Handling |
|---|---|---|
| V-01 | `/UnderGraduate` eligibility text refers to "as on March 2022" and "admission 2022" while the banner says 2026-2027. | **OUTDATED.** Do not republish. Request current eligibility from the admissions office. |
| V-02 | `/UnderGraduate` and `/PostGraduate` mention payment of application fees via "Paytm wallet". | Unverified current practice. Not carried into the new site without confirmation. |
| V-03 | Home page "News" ticker repeats marketing slogans; event cards link to generic pages. Event dates include 18 Jan 2026 on three different cards and a 2 Nov 2026 symposium. | Treat as demo-grade. News/events will start empty or marked demo. |
| V-04 | Home page lists "TCS, Infosys, Cognizant, Wipro, IBM, Mahindra" under "Industry Relation". No MoU, count or year is given. | **Unverified.** Recruiter names are not used as claims until the college provides evidence. |
| V-05 | Department vision/mission texts contain targets such as "100% placement rate" and "40% of the batch securing Super Dream offers" and "ensuring 100% placement". | Aspirational marketing claims. Need explicit approval; not presented as achieved results. |
| V-06 | Chairman page says "Youngest Founder Chairman in India" and "Best Educationist award Winner". | **Unverified superlatives.** Not published without documentary evidence. |
| V-07 | `/Circular` page shows four marketing slogans, no circulars. | **MISSING.** The Circular module starts empty. |
| V-08 | `/Recruitments` contains no placement statistics, recruiter list or year. It describes the TPC as headed by the Vice Principal and uses text referring to "SIT". | **MISSING** statistics. Do not invent any. |
| V-09 | The Mandatory Disclosure PDF (AICTE Form-16) contains data from roughly 2000 to 2008 and 2020 to 2022: affiliation period "2021-2022", fees "for 2008-2009", placement lists for 2000 to 2008 batches, software lists from the early 2000s (Windows 2003 server, JDK 1.3), a 2022 admission calendar, and staff listings with older designations. It also contains individuals' personal details (dates of birth, home addresses and phone numbers). | **OUTDATED, and sensitive.** None of its numbers or personal data may be republished. A current mandatory disclosure must come from the college. |
| V-10 | Page `<title>` and image alt texts are stuffed with search keywords ("Top engineering college chennai", "Padippai college", and so on). Typos exist ("ADMISSIOIN", "Grivance" in the URL path). | Not copied. New site uses clean titles, alt text and corrected spellings. Legacy URLs get redirects. |
| V-11 | `online.skec.edu.in` returned a hosting-panel default page ("Domain Default page" from Plesk) when fetched on the research date. | **UNVERIFIED.** It may reflect a misconfiguration, a maintenance state or the fetch environment. No login was attempted. The college IT team must confirm the portal's real status and URL. The new site links to it only after confirmation. |
| V-12 | `/Prospectus` shows prospectus pages as two JPEG images, so text is not searchable or accessible. | The new site needs the source document (PDF or text) to provide an accessible version. |
| V-13 | `/Administration` holds the objects of the Trust, not a leadership roster. No Principal, Vice Principal, HOD or faculty roster appears on the pages inspected. The PDF names a Principal and Vice Principal, but as of an older date. | **MISSING.** Leadership names require current confirmed data. |
| V-14 | Faculty list is only a linked PDF ("AU-CAISTAFF-PhotoList.pdf"), not fetched. | **NOT-INSPECTED.** |

## 7. Unavailable or unreadable resources

| Resource | Problem |
|---|---|
| Prospectus content | Images only; text cannot be extracted without OCR and a rights decision |
| Exam timetable PDFs, syllabus PDFs, AICTE EOA 2025-26, faculty PDF | Not fetched in this session |
| `online.skec.edu.in` application | Root returns a hosting default page (see V-11); the application itself was not and must not be probed |

## 8. Information required from the college administration

1. Approved programme list with AICTE intake and current approval status (resolves C-01).
2. Official contact details: role-based email addresses, phone numbers, admissions helpline (C-02).
3. Approved Founder Chairman biography, qualification line and permission to publish his photograph.
4. Confirmation of founding history, advisor details and the relationship of SKIT to SKEC (H-01 to H-05, C-05).
5. Current leadership: Principal, Vice Principal, Deans, HODs, with approved photographs and designations.
6. Current admission eligibility, fee structure, dates and process for 2026-2027 (V-01).
7. Placement statistics for the last three academic years with a source document, plus recruiter list with evidence (V-04, V-08).
8. Current mandatory disclosure, AICTE EOA, NAAC/NBA/NIRF status (only if held; none is assumed).
9. Current regulations per batch (C-04) and the exam timetable process.
10. Transport routes and timings, hostel capacity and fees, library statistics, sports facilities list (to replace marketing teasers).
11. Grievance, anti-ragging, internal complaints and other statutory committee details (names, contacts, constitution dates).
12. Status of the existing student portal and whether the new system will replace or coexist with it.

## 9. Publication gate

A content item goes live only when: (a) its source is recorded here, (b) the college has approved it in writing, and (c) it carries an "as of" date where it can change. Until then the item is a placeholder and is excluded from production builds.
