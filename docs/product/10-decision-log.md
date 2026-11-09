# 10 — Product & Engineering Decision Log

Record decisions that are expensive to reverse or affect users, security, architecture, or scope.

## Decision template

### DEC-[NNN]: [Short title]

- **Date:** [YYYY-MM-DD]
- **Status:** Proposed / Accepted / Superseded
- **Owner:** [TBD]
- **Context:** What problem or constraint requires a decision?
- **Options considered:** What realistic alternatives were evaluated?
- **Decision:** What was selected?
- **Rationale:** Why is this the best option now?
- **Trade-offs:** What are we accepting?
- **Consequences:** What must change or be monitored?
- **Review trigger:** What evidence would cause us to revisit it?

---

## Initial decisions

### DEC-001: Keep product definition evidence-led

- **Date:** 2026-11-09
- **Status:** Accepted
- **Owner:** Product owner
- **Context:** Repository name and starter files do not specify the intended product, user, or MVP.
- **Decision:** Keep product-specific fields as TBD until discovery evidence and owner decisions exist.
- **Rationale:** Inventing a product definition would create false requirements and lead implementation in the wrong direction.
- **Consequences:** Complete discovery before locking the PRD, stack, schema, and roadmap.

### DEC-002: Use documentation as a source of truth, not a substitute for validation

- **Date:** 2026-11-09
- **Status:** Accepted
- **Owner:** Product owner
- **Context:** A planning framework can reduce ambiguity but cannot prove demand or guarantee correct code.
- **Decision:** Require user evidence, acceptance criteria, tests, and human review before release.
- **Rationale:** A document-heavy process can waste time if it is not tied to decisions and measurable outcomes.
- **Consequences:** Keep documents concise and update them only when evidence or decisions change.
