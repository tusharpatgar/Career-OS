# Career-OS Product & Build Documentation

This folder is the working source of truth for product discovery, requirements, architecture, delivery, and launch.

## Status

**Planning scaffold — product definition is not yet validated.** The repository name alone does not establish what Career-OS does. Do not infer target users, workflows, business model, or features from the name. Replace every `[TBD]` with evidence-backed decisions before implementation.

## Documents

| Order | Document | Purpose |
|---|---|---|
| 00 | [Product discovery](00-product-discovery.md) | Problem evidence, users, alternatives, validation |
| 01 | [PRD](01-prd.md) | Scope, requirements, user stories, outcomes |
| 02 | [App flow](02-app-flow.md) | Screens, navigation, journeys, states |
| 03 | [UI/UX brief](03-ui-ux-brief.md) | Interaction and visual system |
| 04 | [Technical requirements](04-technical-requirements.md) | Architecture, stack, integrations, constraints |
| 05 | [Data model & security](05-data-model-security.md) | Entities, access rules, privacy and retention |
| 06 | [Implementation plan](06-implementation-plan.md) | Sequenced delivery and acceptance gates |
| 07 | [Quality plan](07-quality-plan.md) | Testing, observability, reliability |
| 08 | [Launch & operations](08-launch-operations.md) | Release, support, incident response |
| 09 | [Cost model](09-cost-model.md) | Build and operating cost assumptions |
| 10 | [Decision log](10-decision-log.md) | Record decisions and their rationale |

## Working rules

1. Evidence before features. Interview and observe intended users; do not treat founder intuition as validation.
2. Keep the first release narrow. Every MVP feature must support the primary user outcome.
3. Mark unknowns as `[TBD]`; never let an AI agent silently invent requirements.
4. Record consequential decisions in the decision log.
5. Update these documents when implementation or user evidence changes the plan.
6. Never put credentials, API keys, real personal data, or production secrets in this repository.
7. Treat generated code as untrusted until reviewed, tested, and checked for security.

## First decisions required

- What specific career-related problem is Career-OS solving?
- Who experiences it most acutely, and who would pay or sponsor the solution?
- What is the single primary outcome the MVP must deliver?
- What evidence demonstrates that this problem is frequent, costly, and underserved?

## Suggested workflow

Discovery → PRD → app flow and UX → technical architecture and data/security model → implementation plan → build in small vertical slices → test → pilot → launch.

Do not spend weeks polishing documents. The purpose is to expose uncertainty and guide a small, testable release—not to create paperwork.
