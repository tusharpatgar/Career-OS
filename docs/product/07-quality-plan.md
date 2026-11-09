# 07 — Quality, Testing & Observability Plan

## 1. Test strategy

| Level | What it verifies | Required for |
|---|---|---|
| Unit | Pure logic and validation | Core business rules |
| Integration | API, database, auth and external boundaries | All persisted workflows |
| End-to-end | User journey from entry to outcome | Primary MVP flows |
| Security | Authorization, input handling, session and dependency risks | All protected workflows |
| Accessibility | Keyboard, semantics, focus, labels, contrast | Primary screens |
| Performance | Response time and resource use under expected load | Critical journeys |

## 2. Acceptance test format

For each PRD requirement define:
- Given: initial state and actor.
- When: action performed.
- Then: expected visible and persisted result.
- Negative case: invalid, unauthorized, or unavailable condition.
- Evidence: automated test or recorded manual test.

## 3. Minimum release checks

- [ ] Fresh install and documented local setup work.
- [ ] Lint, type checks, and automated tests pass.
- [ ] Primary user journey passes end to end.
- [ ] Unauthorized access is denied server-side.
- [ ] Validation and error messages are understandable.
- [ ] No secrets or personal data in repository history.
- [ ] Critical dependencies have no unresolved high-severity known vulnerabilities.
- [ ] Keyboard navigation and core accessibility checks pass.
- [ ] Backup / restore is tested if production data is stored.
- [ ] Monitoring and rollback are ready.

## 4. Observability

Define:
- Application health checks: [TBD]
- Error tracking: [TBD]
- Structured logs: [TBD]
- Product events: only events needed for agreed metrics; avoid unnecessary personal data.
- Alerts and thresholds: [TBD]
- Log retention and access: [TBD]

## 5. Defect severity

| Severity | Meaning | Release response |
|---|---|---|
| Critical | Data breach, data loss, or core system unusable | Stop release; immediate response |
| High | Core workflow materially broken or access control failure | Block release |
| Medium | Important secondary workflow degraded | Fix or explicitly accept with owner |
| Low | Cosmetic / low-impact issue | Backlog with priority |

## 6. Pilot feedback

Capture issue, user context (anonymized), impact, reproducibility, workaround, and decision. Do not treat one anecdote as a universal requirement.
