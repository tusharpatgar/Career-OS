# Career OS — Test Results

## Documentation/configuration milestone
Date: 2026-11-09
Status: Not runtime-tested in this milestone.

Files created/updated: editable source configuration files, configuration instructions, product documentation and persistent project handoff/control files.

## Tests not yet run
- No application config parser exists or has been tested.
- No live scraper adapter tests have been run.
- No company career portal URL health checks have been run.
- No consultancy contact verification has been run.
- No application, email or n8n workflows have been implemented or tested.

## Required next tests
1. Parse comments and blank lines.
2. Parse valid records with exact field counts.
3. Reject malformed rows and invalid booleans.
4. Validate HTTP/HTTPS URLs and reject unsafe schemes.
5. Detect duplicate names and normalized URLs.
6. Reject unknown adapter IDs or mark them pending visibly.
7. Preserve disabled sources without querying them.
8. Report unsupported sources rather than silently skipping them.
9. Test local self-hosted and public per-user overrides.
10. Test merge behavior when repository defaults change.
11. Run adapter health checks with fixtures and permitted live tests.
12. Confirm no secrets or personal data are stored in source files.

Do not mark tests as passed until executed and results are recorded.
