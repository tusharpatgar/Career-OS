# Changelog

## 2026-11-11 — Source parser, adapter registry and GUI shell
- Added `careeros/` Python package (standard library only).
- Added the source configuration parser: comments, blank lines, exact field counts, URL scheme/host/credential validation, strict booleans, duplicate name/URL detection, and per-line `SourceIssue` reports so no configured source is silently skipped.
- Added the layered loader: repository defaults plus an optional user override directory, merged by normalized source name with `origin` provenance.
- Added the adapter registry with health states (supported, pending, disabled, temporarily_unavailable, blocked_or_restricted) and scrapeable filtering. JobSpy is registered as pending because no adapter is implemented.
- Added a read-only web GUI (`python3 -m careeros.web.server`): dashboard of 131 configured sources, status chips, search/status/enabled filters, config-issue list, adapter list and a `/api/snapshot` JSON endpoint that re-reads config on every request.
- Added 48 tests across parser, registry and snapshot layers; all pass.
- Added `pyproject.toml` (pytest configuration) and `docs/run-locally.md`.
- Ignored local dependency and runtime directories in `.gitignore`.
- No scraper, database, authentication, application, email or automation behaviour is claimed implemented.

## 2026-11-09 — Product configuration and AI continuity foundation
- Added editable job-platform, company-portal and recruitment-source text files.
- Added configuration editing, validation, override and safety documentation.
- Added MANGOS employer definition: Microsoft, Amazon, Netflix, Google, Oracle and Salesforce.
- Added permanent handoff, project state, task tracker, decision log, research register and test-results files.
- Added Claude-specific operating instructions.
- No runtime scraper, parser, application or automation behavior is claimed implemented.
