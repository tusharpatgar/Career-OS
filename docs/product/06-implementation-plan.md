# 06 — Implementation Plan

**Status:** Sequencing template; do not start feature development until the discovery gate is met.

## Delivery principles

- Build one end-to-end user workflow at a time.
- Keep pull requests small and reviewable.
- Each task has an owner, acceptance criteria, tests, and rollback consideration.
- Do not ask an AI coding agent to implement the entire product in one prompt.
- Update the docs when decisions change.

## Phase 0 — Validate the problem

**Deliverables:** completed discovery evidence, target segment, problem statement, validation decision.  
**Exit criteria:** discovery go/no-go gate passed.  
**Do not:** build a broad platform based on assumptions.

## Phase 1 — Define the MVP

**Deliverables:** approved PRD, primary journey, out-of-scope list, measurable success metrics.  
**Exit criteria:** every MVP requirement has acceptance criteria.

## Phase 2 — Design and architecture

**Deliverables:** screen flows, UI brief / wireframes, architecture decision, data model, threat model, cost estimate.  
**Exit criteria:** core workflow and data access rules reviewed.

## Phase 3 — Repository and engineering foundation

Tasks:
- Confirm runtime, framework, and package manager.
- Establish folder structure and local setup instructions.
- Add formatting, linting, type checks, and automated tests.
- Configure environment variable validation and safe example config.
- Configure CI and branch protections where appropriate.

**Exit criteria:** a clean clone can install, test, and run locally.

## Phase 4 — Vertical slice 1

Implement the smallest complete primary user journey across UI, API, persistence, authorization, and error handling.

**Exit criteria:** acceptance criteria pass; unauthorized access is tested; no critical security findings.

## Phase 5 — Remaining MVP capabilities

Implement only Must-have requirements in dependency order. Revisit scope when effort exceeds the validation value.

## Phase 6 — Hardening

- Unit, integration, and end-to-end tests.
- Accessibility and responsive checks.
- Security and dependency scans.
- Backup / restore test if persistent production data exists.
- Performance baseline and observability.
- User acceptance testing with target users.

## Phase 7 — Pilot and launch

Release to a small, defined cohort. Monitor the primary outcome, task completion, support burden, and incidents. Decide whether to iterate, expand, or stop.

## Task tracker

| ID | Task | Phase | Priority | Owner | Acceptance criteria | Status |
|---|---|---|---|---|---|---|
| TASK-001 | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | Not started |

## Definition of Done

- Requirement and acceptance criteria are met.
- Code is reviewed and follows project conventions.
- Automated tests pass.
- Authorization and validation are covered.
- No secrets or real personal data are committed.
- Loading, empty, success, and failure states are handled.
- Documentation and operational notes are updated.
- Deployment and rollback impact are understood.
