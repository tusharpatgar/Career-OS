# Career OS — Project State

Last updated: 2026-11-11
Branch: project-creater
Milestone: Source configuration parser, adapter registry and read-only GUI shell

## Current state
- Product direction: AI-assisted job discovery, tailored application preparation, tracking and recruiter outreach.
- Deployment: self-hosted edition plus public frontend with separately hosted backend.
- Planning scaffold: docs/product/.
- Editable source seeds: config/platforms.txt, config/companyportals.txt, config/recruitment_sources.txt.
- Configuration instructions: config/README.md.
- Durable AI handoff: HANDOFF.md.
- Runtime implemented so far: Python package `careeros/` containing the source configuration parser (COS-011), the adapter registry with health states (COS-012) and a stdlib web GUI (`careeros/web/`) that renders parsed sources, statuses and validation issues.
- No scraper adapter is implemented. `jobspy` is registered as **pending** on purpose, so no configured source is reported as supported.
- No candidate onboarding, job records, tracking, documents, email or automation exists yet.

## Verified baseline (2026-11-11)
- `PYTHONPATH=.deps python3 -m pytest -q` → 48 passed.
- GUI loads 131 configured sources: 25 platforms, 82 company portals, 24 consultancies; 0 validation issues; 108 pending, 23 disabled, 0 supported.
- Read-only HTTP API verified locally: `/api/health`, `/api/snapshot`, `/`, `/static/app.js`, `/static/styles.css` all 200.

## Confirmed constraints
- Audit/reuse suitable open-source projects before building replacements.
- Source text files are manually editable and dynamically loaded on every request.
- Source registration does not imply scraper support.
- Database is authoritative; Excel is an export.
- Final application submission and recruiter email sending require explicit approval.
- GitHub Pages is frontend hosting only.
- Support local self-hosted and per-user public configuration overrides.

## Next milestone
Complete the P0 open-source audits (COS-001 … COS-007) and expand/verify source coverage, then implement the first real adapter against the registry and replace the read-only snapshot with database-backed job discovery.

## Risks
- Job-board access and terms change frequently.
- Career portals use different ATS systems and may need individual adapters.
- Company lists become stale without provenance and verification timestamps.
- Browser automation is brittle and can violate source restrictions.
- Public deployment requires strong tenant isolation and secure secret storage.
- The GUI is currently read-only; adding editing requires authentication and per-user override storage before it is exposed publicly.
