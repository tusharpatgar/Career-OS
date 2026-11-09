# Instructions for AI Coding Agents

## Source of truth
- Read `docs/product/README.md` and the relevant product documents before proposing or changing product behaviour.
- These documents are a planning scaffold. Product details marked `[TBD]` are unknown, not permission to invent requirements.
- If a missing decision materially affects implementation, stop and ask the product owner. Offer options with trade-offs rather than silently choosing.

## Engineering behaviour
- Inspect the existing repository and follow its actual stack and conventions; do not assume a framework.
- Prefer the smallest change that satisfies an approved requirement.
- Work in small, reviewable steps. Explain files changed and why.
- Add or update tests for behaviour changes.
- Run relevant tests, lint, and type checks; report exact commands and results.
- Do not claim a test passed unless it was run successfully.
- Do not introduce dependencies without explaining why they are needed.

## Security and privacy
- Never commit credentials, tokens, private keys, production data, or identifiable user research.
- Enforce authorization on the server, not only in the UI.
- Validate untrusted input and handle errors explicitly.
- Minimize personal data collection and logging.
- Do not make consequential employment, promotion, or candidate decisions automatically without explicit requirements, human oversight, transparency, appeal mechanisms, and legal review.

## Git discipline
- Do not force-push or rewrite history.
- Do not modify `main` unless explicitly instructed.
- Keep commits focused and descriptive.
- Never overwrite existing files without inspecting their current contents first.
