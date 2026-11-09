# Instructions for AI Coding Agents

## Mandatory resume procedure
1. Read HANDOFF.md.
2. Read PROJECT_STATE.md, TASK_TRACKER.md, DECISIONS.md, RESEARCH_REGISTER.md and TEST_RESULTS.md.
3. Inspect current branch, working tree, recent commits and repository structure.
4. Resume the first unblocked task. Do not recreate completed work.

## Source of truth
- Product documents live in docs/product/.
- Editable source seeds live in config/platforms.txt, config/companyportals.txt and config/recruitment_sources.txt.
- Read config/README.md before changing their format.
- Text files are user-editable defaults, not proof of scraper support.
- Database is authoritative for jobs, application history, source health and per-user overrides.
- TBD means unknown, not permission to invent.

## Open-source-first policy
- Inspect existing projects before implementing equivalent functionality.
- Record repository URL, inspected revision, license, maintenance, dependencies, test coverage, security, compatibility and reuse/adapt/reject rationale.
- Preserve required licenses and notices.
- Do not copy code with incompatible or unclear licensing.
- Do not claim a source is supported until its adapter has been tested.

## Configuration requirements
- Keep source lists manually editable in UTF-8 plain text.
- Document exact field formats.
- Ignore comments and blank lines; reject malformed records visibly.
- Validate URLs, duplicates, enabled flags and adapter IDs.
- Never silently skip configured sources.
- Support local self-hosted overrides and per-user public-edition overrides.
- Never commit credentials, cookies, API keys, email passwords or personal data.

## Engineering
- Inspect the actual stack; do not assume a framework.
- Prefer the smallest change satisfying an approved requirement.
- Work in small reviewable steps.
- Add/update tests for behavior changes.
- Run relevant tests, lint and type checks; report exact commands and results.
- Never claim a test passed unless it ran successfully.

## Career OS integrity and safety
- Never fabricate candidate experience, skills or qualifications.
- Never mark an application submitted unless confirmed.
- Require explicit approval before final application submission or sending recruiter email.
- Respect site terms, rate limits, authentication boundaries and anti-bot controls.
- Do not bypass CAPTCHA, access controls or paywalls.
- Enforce server-side authorization and per-user data isolation.
- Keep API secrets out of frontend bundles, Git history, logs and config files.
- Treat job and recruiter data as untrusted input.

## Persistent progress / token continuity
After each meaningful milestone update PROJECT_STATE.md, TASK_TRACKER.md, RESEARCH_REGISTER.md, TEST_RESULTS.md, HANDOFF.md and CHANGELOG.md. Before stopping due to context limits, record changed paths, commands, actual test output, blockers and next concrete task. Another model/provider must resume from repository files alone.

## Git discipline
- Work only on the authorized branch, currently project-creater.
- Do not modify main unless explicitly instructed.
- Do not force-push or rewrite history.
- Never push future changes without explicit user approval.
- Inspect existing file contents before updates.
