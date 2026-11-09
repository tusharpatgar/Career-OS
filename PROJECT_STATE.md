# Career OS — Project State

Last updated: 2026-11-09
Branch: project-creater
Milestone: Product direction and editable source configuration foundation

## Current state
- Product direction: AI-assisted job discovery, tailored application preparation, tracking and recruiter outreach.
- Deployment: self-hosted edition plus public frontend with separately hosted backend.
- Existing planning scaffold: docs/product/.
- Editable source seeds: config/platforms.txt, config/companyportals.txt, config/recruitment_sources.txt.
- Configuration instructions: config/README.md.
- Durable AI handoff: HANDOFF.md.
- No runtime parser, scraper, application or automation is claimed complete by this documentation/configuration milestone.

## Confirmed constraints
- Audit/reuse suitable open-source projects before building replacements.
- Source text files are manually editable and dynamically loaded.
- Source registration does not imply scraper support.
- Database is authoritative; Excel is an export.
- Final application submission and recruiter email sending require explicit approval.
- GitHub Pages is frontend hosting only.
- Support local self-hosted and per-user public configuration overrides.

## Next milestone
Audit open-source projects and source directories. Then implement and test the config parser and adapter registry before expanding scraper functionality.

## Risks
- Job-board access and terms change frequently.
- Career portals use different ATS systems and may need individual adapters.
- Company lists become stale without provenance and verification timestamps.
- Browser automation is brittle and can violate source restrictions.
- Public deployment requires strong tenant isolation and secure secret storage.
