# ADR 0002: Core Data Model Baseline

- **Status**: Accepted
- **Date**: 2026-02-13
- **Owners**: Architecture, Backend Engineering, Data + Integrations

## Context
InventoryK12 needs a scalable domain model for assets, assignments, audits,
incidents, and related workflows. Early implementation details are still
emerging, and locking the full schema now would likely create rework and
premature constraints.

## Decision
Adopt an incremental, domain-by-domain data modeling strategy instead of
approving a fully locked schema up front.

Modeling strategy:
1. Implement one domain area at a time (for example: assets, assignments,
   audits, incidents).
2. For each domain area, define only the fields, relationships, and constraints
   required for current milestone scope.
3. Record material design decisions in follow-up ADRs before or during
   implementation.
4. Evolve models through additive, backward-compatible changes where possible.
5. Revisit cross-domain consistency at milestone boundaries.

Design principles:
- Prefer clear domain boundaries over early over-normalization.
- Optimize for auditability and chain-of-custody requirements.
- Keep room for scale and adaptability without speculative complexity.
- Align entity and field naming with `docs/standards/data.md`.
- Keep RBAC and security implications aligned with `docs/standards/security.md`.

Planned follow-up ADR areas:
- Asset entity/model v1
- Assignment and custody model v1
- Audit/discrepancy model v1
- Incident lifecycle model v1
- Organization/location hierarchy model v1

## Consequences
- Reduces up-front design lock-in and allows faster milestone delivery.
- Requires discipline to capture decisions incrementally in ADRs.
- Increases need for migration hygiene and cross-domain review as models evolve.

## Alternatives Considered
- Fully define and approve the entire MVP schema before implementation.
- Delay all architecture decisions until code implementation is complete.

## Follow-Up
- Create domain-specific ADRs as each model area enters active implementation.
- Add migration and compatibility checks per domain as models stabilize.
- Reassess this strategy after Milestone 1 and either keep, amend, or deprecate it.

## Related
- `docs/overview/roadmap.md` (Milestone 0 ADR finalization, Milestone 1 implementation)
- `docs/overview/inventoryk12-blueprint.md` (domain concepts and MVP workflows)
- `docs/adr/0001-auth-strategy.md`
- `docs/adr/0003-ingestion-architecture.md`

## References
- `docs/standards/data.md`
- `docs/standards/migrations.md`
- `docs/standards/security.md`
