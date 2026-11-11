# Career OS — Test Results

## Milestone: source parser, adapter registry and GUI shell
Date: 2026-11-11
Status: **Executed and passing locally.** No live network or scraper tests were run.

### Environment
- Python 3.12.3 (VM interpreter).
- pytest 9.2.0 installed into a project-local `.deps/` directory (`.deps/` and `.venv/` are git-ignored).
- No application dependencies beyond the standard library.

### Commands and actual results

```
$ PYTHONPATH=.deps python3 -m pytest -q
................................................
48 passed
PYTEST_EXIT=0
```

```
$ PYTHONPATH=.deps python3 -m pytest -q
```
(first run: 1 failed, 47 passed — `test_snapshot_surfaces_invalid_rows_instead_of_dropping_them`
expected only row-level issues, but the snapshot correctly also reported the two
absent source files as `missing_file`. The fixture was completed with empty
placeholder files for the other two kinds; the assertion was not weakened.)

### GUI smoke checks (local HTTP, 2026-11-11)

```
GET /api/health          → 200 application/json
GET /                   → 200 text/html; charset=utf-8
GET /static/app.js       → 200 text/javascript; charset=utf-8
GET /static/styles.css   → 200 text/css; charset=utf-8
GET /api/snapshot        → 200
  total: 131
  summary: supported 0, pending 108, disabled 23,
           temporarily_unavailable 0, blocked_or_restricted 0
  issues: 0
  kinds: platform 25, company_portal 82, recruitment 24
  adapters: jobspy → pending
```

Server started with `python3 -m careeros.web.server --host 0.0.0.0 --port 3000`.
The page was rendered in the freebuff Browser panel by the user-facing dev-server
preview; no automated browser interaction test (clicks, filters) has been run.

### Covered by automated tests
1. Comments, blank lines and surrounding whitespace are ignored.
2. Exact field counts per spec; malformed rows are rejected with `wrong_field_count`.
3. Empty names and empty adapter IDs are rejected.
4. `enabled` accepts only case-insensitive true/false (`invalid_enabled` otherwise).
5. URLs must be http/https with a host, no whitespace/control characters, no embedded credentials; `javascript:`, `file:` and `ftp:` are rejected.
6. Duplicate names (case/whitespace-insensitive) and duplicate URLs (normalized scheme/host/path) are rejected with line references.
7. Disabled sources are preserved, never dropped.
8. The real `config/*.txt` seed files parse with zero issues (25 / 82 / 24 records).
9. Missing or unreadable source files are reported (`missing_file`, `unreadable_file`) instead of silently skipped.
10. Override layering replaces entries by name, appends new entries, marks `origin: override`, reports cross-layer duplicate URLs, and tolerates an absent override directory.
11. Adapter registry rejects invalid IDs, unknown health states, empty kind sets and duplicate registrations.
12. Status resolution covers supported, pending (unknown adapter / kind mismatch / no adapter assigned), disabled and adapter health (`temporarily_unavailable`, `blocked_or_restricted`).
13. Only `supported` records are returned as scrapeable; disabled sources are never returned.
14. `default_registry()` reports `jobspy` as pending, so no seeded source is claimed as supported.
15. Snapshot builder is JSON serializable, exposes per-record provenance (file and line) and adapter metadata, and honours the override layer.

## Not yet run
- No live scraper, job-board or career-portal request has been made.
- No company career portal URL health checks.
- No consultancy contact verification.
- No authentication, write path, database, n8n or email tests (none implemented).
- No automated browser E2E test of the GUI filters/tabs (verified by API and manual preview only).
