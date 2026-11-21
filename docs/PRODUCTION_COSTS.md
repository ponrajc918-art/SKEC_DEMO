# Production Costs, Environment and Security Requirements

Phase 0 deliverable. This document lists **categories** of production cost and the factors that drive them. It deliberately contains **no price quotations**: prices change, vary by provider and region, and no vendor quotation was obtained in Phase 0. Verify current pricing with each vendor before budgeting.

**The production system will not be free.** The software stack is open source, but hosting, backups, email delivery, domain and certificate management, payment-gateway fees, security review and people's time all cost money.

## 1. Cost categories

| # | Category | What it covers | Cost driver | Free option exists? | Note |
|---|---|---|---|---|---|
| 1 | Software licences | Next.js, React, FastAPI, PostgreSQL, Docker, Tailwind, shadcn/ui, Pytest, Playwright | None | Yes, all open source | Fonts (Source Serif 4, Inter) are also open licence |
| 2 | Application hosting | Server or container platform for frontend, backend, worker | Compute size, uptime target, region | Free tiers exist but are unsuitable for a production ERP with student data | Prefer India region |
| 3 | Database hosting | PostgreSQL managed service or self-managed server | Storage, memory, high availability, backups | Self-managed on own server costs only server and staff time | Managed service reduces operations risk |
| 4 | Object storage | Question papers, uploads, gallery, receipts | Stored volume, requests, transfer | Self-hosted MinIO uses server disk | Needs backup and encryption |
| 5 | Backups and disaster recovery | Nightly dumps, off-site copy, restore drills | Data volume, retention | Partly (own scripts) | Backups on the same host are not a backup |
| 6 | Domain and DNS | `skec.edu.in` already used by the college; subdomains for staging and API | Registrar rules for `.edu.in` | n/a | Confirm who controls DNS |
| 7 | TLS certificates | HTTPS | None with Let's Encrypt | Yes | Automate renewal |
| 8 | CDN and edge protection | Caching, DDoS and bot protection | Traffic, plan tier | Limited free tiers | Review limits against admission-season traffic |
| 9 | Email delivery | Transactional email (credentials, receipts, circulars) | Monthly volume, domain reputation set-up (SPF, DKIM, DMARC) | Limited free tiers | Bulk circulars can exceed free limits |
| 10 | SMS / WhatsApp | OTP, alerts | Per-message fees; Indian telecom rules require registration of senders and templates | No | Optional, college decision |
| 11 | Payment gateway | Razorpay fees per transaction, possible set-up and settlement terms | Transaction value and volume, payment methods | Test mode is free; live mode is charged per transaction | Live mode needs authorised college credentials and approval |
| 12 | Monitoring and logging | Uptime checks, error tracking, log retention | Event volume, retention | Free tiers and open-source stacks exist | Keep personal data out of logs |
| 13 | Security assurance | Independent penetration test, dependency monitoring, security training | Scope, tester rates | Automated scanning is free; a professional penetration test is not | Recommended before go-live |
| 14 | Legal and compliance | Review against the Digital Personal Data Protection Act, 2023, privacy policy, terms, consent for minors, payment terms | Counsel time | No | Needs the college's legal adviser |
| 15 | Content and media | Professional photography, videography, prospectus design, accessibility-compliant PDFs | Shoot days, editing, licensing | No | Images are replaced after the platform is built (ASSET_MANIFEST.md) |
| 16 | Data migration | Import of official exports from the existing system, if provided | Data quality and volume | Own tooling | Not assumed |
| 17 | Training and handover | Staff training, user guides, helpdesk set-up | Number of roles and sessions | Self-produced material | Needed for adoption |
| 18 | Ongoing operations | Patching, updates, support, incident response, yearly security review | Hours per month, response expectations | No | The largest recurring cost is usually people |
| 19 | Contingency | Unplanned usage spikes, extra storage, extra integrations | Risk appetite | n/a | |

## 2. Cost scaling considerations

- **Admission season** produces traffic peaks on the public site; fee deadlines produce peaks on payments; result publication produces peaks on student portal logins. Size and test for these (Phase 6 load tests).
- **Storage grows** with question papers, gallery photographs, assignment submissions and receipts over the years.
- **Redundancy** (a standby database, multiple application instances) improves uptime and raises cost; the college should choose a target uptime deliberately.
- A **small initial deployment** (one server running Docker Compose with off-host backups) is the lowest-cost viable start; move to managed services if operational capacity is limited.

## 3. Environment configuration

- All configuration comes from environment variables listed in `.env.example`, which contains placeholders only.
- Three environments: development, staging, production, each with separate databases, buckets, secrets and payment keys.
- Production secrets live in the hosting provider's secret store or an encrypted file on the server, not in the repository, ZIP archives or chat.
- Payment mode is `test` everywhere until the college approves go-live in writing; switching to `live` is an audited administrative action plus a deployment configuration change.

## 4. Security requirements checklist (production gate)

| Area | Requirement |
|---|---|
| Transport | HTTPS only, HSTS, modern TLS |
| Authentication | Argon2id, mandatory MFA for principal, HOD, college admin and finance admin, rate limiting and lockout |
| Sessions | HttpOnly, Secure, SameSite cookies, idle and absolute timeouts, server-side revocation |
| Authorisation | Backend-enforced RBAC with scopes; automated tests for every permission rule |
| Data | Encryption at rest for database volumes and object storage; application-level encryption for any sensitive fields |
| Files | Private buckets, signed short-lived URLs, malware scanning, type and size limits |
| Audit | Append-only audit log, reviewed regularly |
| Web hardening | CSP, security headers, input validation, output encoding, CSRF protection |
| Dependencies | Lockfiles, vulnerability scans, scheduled updates |
| Backups | Encrypted, off-host, restore tested before go-live and at least yearly |
| Monitoring | Alerts for error spikes, repeated failed logins, payment webhook failures |
| Payments | Server-side amount calculation, signature and webhook verification, idempotency, reconciliation; no card data stored |
| Privacy | Data minimisation, retention schedule, consent for minors, privacy notice, a named contact for data requests |
| Access control for operators | Least privilege for servers and databases, separate migration role, shared accounts forbidden |
| Incident response | Written plan, contact list, breach-notification procedure reviewed with the college |

## 5. Deployment architecture options

| Option | Description | Strengths | Weaknesses |
|---|---|---|---|
| A. Single server | One virtual server in an Indian region running Docker Compose (proxy, frontend, backend, PostgreSQL, MinIO, worker) with off-host backups | Lowest cost, simple | Single point of failure, manual scaling, requires an operator |
| B. Managed database and storage | Application containers on one or two servers; managed PostgreSQL and S3-compatible storage | Better durability and backups | Higher cost |
| C. Managed container platform | Containers on a managed platform with managed data services | Least operational effort, easy scaling | Highest cost, provider lock-in considerations |

The recommended starting point is **A or B**, chosen with the college in Phase 5 after confirming budget, operator availability and uptime expectations. No hosting provider has been selected or contacted.

## 6. What the project owner must decide

1. Who operates the system after delivery (college IT, the agency, or a vendor).
2. Target uptime and acceptable downtime windows.
3. Budget band for hosting and recurring services.
4. Whether SMS or WhatsApp notifications are wanted.
5. Who holds the Razorpay account and approves live payments.
6. Who owns the domain, DNS and the email sending domain.
