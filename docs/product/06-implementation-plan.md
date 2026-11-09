# 06 — Implementation Plan

**Status:** Product direction established; implementation sequence subject to repository and open-source audit.

## Delivery principles
- Build one end-to-end workflow at a time.
- Reuse open-source projects when licensing, maintenance, security and architecture are compatible.
- Keep changes small and reviewable.
- Every task needs acceptance criteria and tests.
- Update state, tracker, research, test results and handoff after each milestone.

## Phase 0 — Open-source and source research
- Inspect JobSpy, job-hunter, LinkedIn-Job-Scraper, career-ops, ai-job-search and ai-job-search-au.
- Identify and evaluate Agent-Reach and adjacent open-source tools.
- Record revision, license, maintenance, dependencies, supported sources, tests, security and reuse decision.
- Research Indian job platforms, IT employers, MANGOS companies, career portals and consultancies.
- Populate source seeds with provenance and verification status.

Exit: research register contains evidence-based decisions; no unverified source is represented as a working scraper.

## Phase 1 — Validate the MVP
Define target user, primary problem, workflow, validation evidence and success metrics.

## Phase 2 — Candidate profile and documents
Implement onboarding, resume upload/parsing, editable profile and secure document storage.

## Phase 3 — Job discovery and adapters
- Define a common adapter interface.
- Load config/platforms.txt and config/companyportals.txt dynamically.
- Parse comments, blank lines, exact field counts, enabled flags and URLs.
- Validate and deduplicate source entries.
- Report unsupported sources; never silently skip.
- Add health checks, retries, rate limits and last-checked timestamps.
- Prefer APIs/structured feeds; use browser automation only where appropriate and permitted.

Exit: fixtures cover valid, malformed, duplicate, disabled, pending and unavailable sources; enabled adapters have integration tests.

## Phase 4 — Matching and tracker
Normalize jobs, deduplicate across sources, score against candidate preferences, persist status history and export Excel. Distinguish discovered, shortlisted, prepared, apply-page-opened, submitted-confirmed, interview, rejected and offer.

## Phase 5 — Tailored application documents
Preserve original job descriptions. Generate ATS-oriented resumes, cover letters and answers from verified candidate information only. Detect fabricated claims and version documents per job.

## Phase 6 — User-authorized application assistance
Assist with supported form fields. Require explicit confirmation before final submission. Never bypass CAPTCHA, authentication, access controls or anti-bot protections.

## Phase 7 — Daily automation and recruiter outreach
Use self-hosted n8n for orchestration. Keep the database authoritative. Make reruns idempotent. Verify recruiter contact provenance and require approval before sending email.

## Phase 8 — Deployment
Package self-hosted mode with persistent storage and local config overrides. Public mode needs authentication, tenant isolation, hosted backend, database, workers, file storage and secret management.

## Phase 9 — Hardening
Run unit, integration, E2E, Chromium, accessibility, security, dependency, backup/restore and recovery tests.

## Definition of Done
Acceptance criteria pass; code reviewed; automated tests run and recorded; authorization and validation covered; no secrets committed; failure states handled; docs and tracker updated; deployment and rollback understood.
