# 05 — Data Model, Privacy & Security

**Status:** No production schema approved.

## 1. Data inventory

| Data element | Why needed | Source | Sensitivity | Retention | Deletion method |
|---|---|---|---|---|---|
| [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

Collect the minimum data needed for a defined purpose. Do not collect sensitive employment, identity, financial, or health data simply because it might be useful later.

## 2. Entity catalogue

| Entity | Purpose | Key fields | Relationships |
|---|---|---|---|
| [TBD] | [TBD] | [TBD] | [TBD] |

For each entity specify:
- Primary key and identifier strategy.
- Required / optional fields and validation.
- Foreign keys and deletion behaviour.
- Unique constraints and indexes.
- Created / updated timestamps.
- Audit requirements.

## 3. Authorization matrix

| Actor / role | Resource | Read | Create | Update | Delete / export |
|---|---|---:|---:|---:|---:|
| Anonymous | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Authenticated user | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Administrator | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

Authorization must be enforced server-side. Hiding a button is not access control.

## 4. Security baseline

- Deny by default; grant least privilege.
- Enforce authorization on every protected server operation.
- Validate input on the server; encode output appropriately.
- Use secure session and cookie settings appropriate to the chosen stack.
- Store secrets in environment-specific secret management; never commit them.
- Encrypt data in transit; evaluate encryption at rest and field-level needs.
- Protect against injection, XSS, CSRF, SSRF, insecure direct object references, and brute force as applicable.
- Rate-limit authentication and sensitive endpoints.
- Keep dependencies patched; scan dependencies and secrets.
- Log security events without leaking credentials or sensitive payloads.
- Back up production data and test restoration.

## 5. Privacy and governance

Before handling real user data, determine applicable Indian and other jurisdictional privacy requirements with qualified counsel. Document:
- Purpose and lawful basis / consent model as applicable.
- User notice and transparency.
- Data access, correction, export, and deletion workflows.
- Retention schedule and deletion verification.
- Processor / vendor list and data locations.
- Incident notification obligations.
- Special handling for minors or sensitive data, if relevant.

## 6. Threat model

| Threat | Asset / impact | Mitigation | Verification |
|---|---|---|---|
| Unauthorized access across accounts | User data exposure | Server-side ownership checks / row-level policies | Negative authorization tests |
| Credential leakage | Account compromise | Secret manager, rotation, scanning | Secret scan |
| Malicious input | Data or account compromise | Validation, encoding, parameterized queries | Security tests |
| Excessive privilege | Broad data exposure | Least privilege and role review | Permission matrix tests |
| Data loss | User harm / downtime | Backups and restore drills | Restore test |

## 7. Special caution for career and employment data

If Career-OS processes resumes, employment history, performance feedback, promotion information, or other career-related records:
- Treat these as sensitive personal information in practice.
- Do not expose one employer's or user's records to another tenant.
- Do not infer or score protected characteristics.
- Do not automate consequential employment decisions without rigorous validation, human review, transparency, appeal paths, and legal review.
- Keep provenance and audit trails for consequential changes.
- Define deletion and retention rules before collecting data.

## 8. Schema approval gate

No production migration until entities, ownership, authorization, retention, and deletion behaviour have been reviewed.
