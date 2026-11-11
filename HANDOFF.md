# Career OS — Permanent AI Handoff

Read this file before doing any work. Repository files are the durable project memory; do not depend on chat history.

## Repository
- Product: Career OS
- Repository: https://github.com/tusharpatgar/Career-OS
- Working branch: project-creater
- Default branch: main; do not modify without explicit approval.
- Previous base commit before this configuration update: f4c2d4c16cd074ed3444761332b0f016139806ae

## Product direction
AI-assisted job-search operating system: candidate profile and resume onboarding; job discovery; scoring and deduplication; tailored resumes, cover letters and application answers; persistent tracker and Excel export; user-authorized application assistance; recruiter research and outreach.

Two editions:
1. Self-hosted: local machine or user-managed infrastructure with persistent database, workers, optional Chromium and n8n.
2. Public web: static frontend where appropriate plus separately hosted backend, database, authentication, file storage, workers and secret storage. GitHub Pages cannot host backend services or secrets.

## User-editable source lists
- config/platforms.txt — job boards/platforms.
- config/companyportals.txt — official company career portals.
- config/recruitment_sources.txt — consultancies and staffing firms.
- config/README.md — format, editing and safety instructions.

All source files are UTF-8 plain text with documented pipe-delimited formats. Users can edit them in a text editor and commit/push. The app must dynamically parse, validate and load them. A URL is not proof of a working scraper. Support local self-hosted overrides and per-user public-edition overrides.

## MANGOS and India employer coverage
For this project MANGOS means Microsoft, Amazon, Netflix, Google, Oracle and Salesforce. Also research Meta, Apple, NVIDIA, OpenAI, Anthropic, SpaceX, major Indian IT services firms, product/SaaS companies, fintechs, startups and GCCs. Current company list is a starter seed, not an exhaustive census of Indian IT companies. Expand with provenance and verification dates; never claim completeness without evidence.

## Open-source-first audit targets
- https://github.com/speedyapply/JobSpy
- https://github.com/jmopr/job-hunter
- https://github.com/arshka/LinkedIn-Job-Scraper
- https://github.com/career-ops-hq/career-ops
- https://github.com/ai-job-search-dev/ai-job-search
- https://github.com/RinaldoG/ai-job-search-au
- Agent-Reach: identify and verify the canonical repository before evaluation.

Record inspected revision, license, maintenance, capabilities, dependencies, tests, security and reuse/adapt/reject decision. Do not duplicate functionality before the audit.

## Core requirements
1. Candidate onboarding and resume parsing.
2. Job discovery via APIs and tested source adapters.
3. India-wide IT employer and company portal research.
4. Job normalization, matching, ranking and deduplication.
5. Excel export and persistent application tracker.
6. Tailored ATS resumes, cover letters and application answers based only on verified candidate information.
7. Browser form assistance with explicit final submission confirmation.
8. Daily discovery using self-hosted n8n.
9. Consultancy discovery and recruiter email preparation with explicit send approval.
10. Evaluate https://antijobboard.com/ for hiring-data utility, access, quality and terms.
11. Self-hosted and public-web editions.
12. Thorough unit, integration, E2E, Chromium, security and recovery testing.

## Non-negotiable rules
- Never invent candidate skills, credentials or work history.
- Never mark an application submitted without confirmation.
- Never send recruiter emails or submit applications without explicit authorization.
- Respect site terms, rate limits, robots directives where applicable and access controls.
- Do not bypass CAPTCHAs or anti-bot protections.
- Never commit secrets, cookies, credentials or personal data.
- Enforce per-user data isolation.
- n8n orchestrates; the application database remains authoritative.

## Token/provider continuity
When context is running low:
1. Stop starting new tasks.
2. Update PROJECT_STATE.md, TASK_TRACKER.md, RESEARCH_REGISTER.md, TEST_RESULTS.md, HANDOFF.md and CHANGELOG.md.
3. Record exact changed paths, commands run, actual test output, failures and blockers.
4. Write one precise next action.
A new Claude session or another model/API provider must read these repository files and resume without recreating completed work.

## Implemented runtime (2026-11-11)
- `careeros/sources/parser.py` — spec-driven parser for the three config files: comments, blanks, exact field counts, name/URL/boolean/adapter validation, duplicate detection, `SourceIssue` reports with file and line.
- `careeros/sources/loader.py` — repository defaults plus optional override directory, merged by normalized source name with `origin` provenance.
- `careeros/sources/registry.py` — adapter registry and health states; only `supported` is scrapeable. `jobspy` is deliberately `pending` (no adapter implemented).
- `careeros/web/` — read-only GUI + `/api/snapshot` JSON, standard library only. Start: `python3 -m careeros.web.server --port 8000`.
- Tests: `PYTHONPATH=.deps python3 -m pytest -q` → 48 passed. See TEST_RESULTS.md for exact output.
- Run instructions: docs/run-locally.md. Decisions: DEC-011 … DEC-014.
- Current live snapshot: 131 sources (25 platforms / 82 portals / 24 consultancies), 0 validation issues, 108 pending, 23 disabled, 0 supported.

## Next tasks
1. Audit all listed open-source projects and Agent-Reach (COS-001 … COS-007); record evidence in RESEARCH_REGISTER.md and record the reuse decision.
2. Expand and verify Indian IT company, job platform and consultancy lists (COS-008 … COS-010).
3. Decide the full application stack in docs/product/04-technical-requirements.md before adding a database or API framework (DEC-011 is scoped to the source layer only).
4. Implement one tested adapter behind the existing registry interface, then set its health to `supported` only when tests pass.
5. Implement one working job discovery vertical slice: adapter → normalized job record → dedupe → DB.
6. Update tracker, tests, state and handoff after every milestone.

## Git approval
The user authorized this specific configuration and handoff update to project-creater. This does not authorize future pushes. Show changes and obtain approval for future pushes. Never push to main without explicit instruction.
