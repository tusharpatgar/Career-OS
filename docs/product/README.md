# Career-OS Product & Build Documentation

## Current product direction
Career OS is an AI-assisted job-search operating system. It onboards a candidate profile and resume, discovers jobs from configurable platforms and official employer career portals, scores and deduplicates opportunities, prepares tailored application documents, tracks activity, and supports user-authorized application and recruiter outreach workflows.

Two deployment editions:
- Self-hosted edition for local machines or user-managed infrastructure.
- Public web edition with a static frontend where suitable (for example GitHub Pages) and separately hosted backend, database, workers and secret storage.

## Source of truth and configuration
- Product requirements and decisions live in this folder and root project-control files.
- User-editable source seeds live in config/platforms.txt, config/companyportals.txt and config/recruitment_sources.txt.
- See config/README.md for formats and editing instructions.
- Text files are seed/default configuration, not proof that a source has a functioning scraper.
- Database is authoritative for job records, application status, source health and per-user overrides.

## Documents
| Order | Document | Purpose |
|---|---|---|
| 00 | Product discovery | Problem evidence, users, alternatives, validation |
| 01 | PRD | Scope, requirements, user stories, outcomes |
| 02 | App flow | Screens, navigation, journeys, states |
| 03 | UI/UX brief | Interaction and visual system |
| 04 | Technical requirements | Architecture, stack, integrations, constraints |
| 05 | Data model & security | Entities, access rules, privacy and retention |
| 06 | Implementation plan | Sequenced delivery and acceptance gates |
| 07 | Quality plan | Testing, observability, reliability |
| 08 | Launch & operations | Release, support, incident response |
| 09 | Cost model | Build and operating cost assumptions |
| 10 | Decision log | Record decisions and rationale |

## Working rules
1. Validate the highest-risk assumptions with users and live source tests.
2. Keep the first release narrow.
3. Mark unknowns as TBD; never let an AI agent silently invent requirements.
4. Record consequential decisions.
5. Never commit credentials, API keys, real personal data or production secrets.
6. Treat generated code as untrusted until reviewed and tested.
7. Reuse compatible open-source projects before writing replacements; audit licenses and maintenance first.
8. Never mark an application submitted unless submission is confirmed.
9. Require explicit user confirmation before sending recruiter emails or submitting applications.

## Important constraints
GitHub Pages can host a static frontend; it cannot host backend, database, Selenium/Chromium workers, n8n or secrets. The public edition needs separately hosted backend infrastructure.

A website added to a source file is not automatically scrapeable. It needs a registered, tested adapter and permitted access method.
