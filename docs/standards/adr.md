# ADR Standards

Use ADRs to record architecture and design decisions with lasting impact.

## File Naming

- Use sequential numeric prefixes: `docs/adr/NNNN-short-title.md`.
- Use kebab-case for the title suffix.
- Do not rename existing ADR files after merge.

## Status Lifecycle

- Allowed statuses: `Proposed`, `Accepted`, `Rejected`, `Deprecated`.
- `Proposed`: under review, not yet policy.
- `Accepted`: active decision for implementation.
- `Rejected`: reviewed and intentionally not adopted.
- `Deprecated`: previously accepted but superseded or retired.
- AI companions should keep ADRs as `Proposed` by default.
- AI companions may set `Accepted` only when explicitly instructed by the
  project owner/user in the active task context.

## Metadata Requirements

- Include metadata bullets at top:
  - `Status`
  - `Date` (`YYYY-MM-DD`)
  - `Owners` (team names or named owners)
- Include these sections:
  - `Context`
  - `Decision`
  - `Model and Field Breakdown` (for domain-model ADRs)
  - `Consequences`
  - `Alternatives Considered`
  - `Follow-Up`
  - `Related`
  - `References`
- For domain-model ADRs, also include:
  - `Domain Review Sign-off Checklist`

## Follow-Up ADR Conventions

- Use follow-up ADRs when a decision is materially expanded, constrained, or changed.
- Prefer focused ADRs by domain area (`assets`, `assignments`, `audits`, `incidents`).
- Title conventions for follow-up decisions:
  - `ADR NNNN: Assets Model v1`
  - `ADR NNNN: Assignment and Custody Model v1`
  - `ADR NNNN: Audit Scope and Discrepancy Model v1`
- In follow-up ADRs, add links to prior ADRs in `Related`.

## Superseding and Amendments

- For material changes, create a new ADR and reference the older ADR.
- Mark older ADR as `Deprecated` only when no longer governing behavior.
- For non-material clarifications, update the existing ADR and keep status unchanged.

## Merge and Review Rules

- Architecture-impacting PRs should include ADR updates when applicable.
- ADR changes should be reviewed for consistency with:
  - `docs/overview/roadmap.md`
  - `docs/overview/*`
  - `docs/standards/*`
  - relevant runbooks and security docs
