# Career OS — Decision Log

## DEC-001 — Product direction
Accepted. Career OS is an AI-assisted job-search operating system covering candidate setup, job discovery, matching, tailored documents, tracking, application assistance and recruiter outreach.

## DEC-002 — Two deployment editions
Accepted. Provide self-hosted and public web editions. GitHub Pages may host a static frontend only; backend, database, workers and secrets require separate hosting.

## DEC-003 — Open-source-first implementation
Accepted. Audit existing GitHub projects and reuse/adapt where license, maintenance, security and architecture permit. Build only missing functionality.

## DEC-004 — Editable source files
Accepted. Use plain UTF-8 pipe-delimited files under config/: platforms.txt, companyportals.txt and recruitment_sources.txt. Users can edit and push them. The app must validate and load them dynamically.

## DEC-005 — Source URL is not scraper support
Accepted. A source must map to a registered, tested adapter and pass health checks before being treated as supported.

## DEC-006 — Per-user overrides
Accepted. Repository files are shared defaults. Self-hosted users may override locally; public users need account-scoped overrides. One user's changes must not affect another.

## DEC-007 — Database is system of record
Accepted. Database owns job records, application history, source health and user overrides. Excel is an export, not the primary database.

## DEC-008 — Human approval for external actions
Accepted. Final application submission and recruiter email sending require explicit user approval. Opening an application form is not proof of submission.

## DEC-009 — MANGOS definition
Accepted. MANGOS means Microsoft, Amazon, Netflix, Google, Oracle and Salesforce. Other major technology employers are listed separately.

## DEC-010 — Durable AI handoff
Accepted. Repository project-control files are durable memory across Claude sessions and model/API provider changes.
