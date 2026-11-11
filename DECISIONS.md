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

## DEC-011 — Python standard library for the source layer and GUI shell
Accepted for this milestone only. The source configuration parser, adapter registry and first GUI are implemented in Python 3.11+ using only the standard library (`http.server`, `json`, `urllib`), with pytest as the sole development dependency.
Rationale: the audited discovery tool (JobSpy) and the planned Excel export are Python; a zero-dependency layer can be run and tested immediately on any machine and keeps the open-source audit reversible.
Trade-off: a hand-written HTTP handler is not a production web framework. The full application stack (frontend framework, API framework, database, auth, hosting) remains **TBD** in docs/product/04-technical-requirements.md and must be decided deliberately.

## DEC-012 — Strict, visible configuration validation
Accepted. Parsing rejects rather than repairs: wrong field counts, empty names, empty adapter IDs, non-boolean `enabled` values and non-http(s) URLs (including embedded credentials) produce `SourceIssue` records with file and line. Duplicate names (case/whitespace-insensitive) and duplicate normalized URLs are rejected. Rejected rows are surfaced in the GUI issue list; nothing is silently dropped. Comments and blank lines are ignored.

## DEC-013 — No support claim without a tested adapter
Accepted. `default_registry()` registers `jobspy` with health `pending` and notes pointing at COS-001. The seeded Naukri/Indeed/Glassdoor rows therefore display as pending, not supported. Supported status requires an implemented adapter whose health is explicitly set to `supported` after tests pass.

## DEC-014 — Read-only GUI until authentication exists
Accepted. The dashboard loads configuration but cannot write it. Editing sources through the UI requires an authenticated write path and per-user override storage (COS-025); shipping an unauthenticated editor would let any visitor rewrite a public edition's source list.
