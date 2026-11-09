# Claude Instructions — Career OS

Before doing any work:
1. Read HANDOFF.md.
2. Read PROJECT_STATE.md, TASK_TRACKER.md, DECISIONS.md, RESEARCH_REGISTER.md and TEST_RESULTS.md.
3. Read AGENTS.md and relevant docs/product/ files.
4. Inspect current branch, git status, recent commits and repository structure.

## Work style
- Continue from the recorded next task; do not restart or recreate completed work.
- Audit existing open-source projects before implementing equivalent functionality.
- Record exact repository revisions, licenses, maintenance, dependencies, tests, security and reuse decisions.
- Keep user-editable source lists in config/; read config/README.md before changing their format.
- A source URL does not imply a working scraper. Unsupported sources must be visible.
- Use small, testable changes and update tests with code.
- Do not invent candidate details or claim tests passed without running them.
- Require explicit user approval before final application submissions or recruiter emails.
- Never commit secrets, cookies, personal data or credentials.

## Token/context handoff
After every meaningful milestone update PROJECT_STATE.md, TASK_TRACKER.md, RESEARCH_REGISTER.md, TEST_RESULTS.md, HANDOFF.md and CHANGELOG.md. If nearing context limits, stop and write a precise handoff with completed work, changed paths, commands, test output, blockers and next action. Another model/provider must resume from repository files.

## Git
Current working branch: project-creater. Never modify main without explicit user instruction. Never push without explicit approval. Do not force-push.
