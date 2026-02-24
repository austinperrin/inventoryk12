# ADR 0009: Domain ADR Decomposition Policy v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering, Docs + Standards

## Context
InventoryK12 domain modeling is progressing with AI companions and frequent
schema iteration. Drift risk increases when one broad ADR governs many domains
without domain-specific guardrails and review checkpoints.

## Decision
1. Maintain one domain ADR per active implementation domain for milestone work.
2. Keep domain ADR status `Proposed` while models are actively reviewed and
   updated; mark `Accepted` only when review gates are complete.
3. Treat roadmap domain checklist items as review gates, not implementation
   toggles. Checklist status is based on explicit review completion.
4. Require domain ADR updates whenever model fields, constraints, ownership, or
   migration intent materially change.
5. Keep identifier contract explicit in each domain ADR:
   internal key is `id` (`BigAutoField`), external API identifier is `uuid`.
6. Require each domain ADR to include a model/field inventory section that
   documents current implemented models and field breakdowns (or explicitly
   marks scaffold domains with planned provisional model fields).

## Consequences
- Reduces scope ambiguity and model placement drift.
- Improves traceability from code/migrations to approved decisions.
- Adds lightweight ADR maintenance overhead during active development.

## Alternatives Considered
- Continue with a small set of broad ADRs only.
- Track domain decisions only in roadmap checklist notes.

## Follow-Up
- Draft domain ADRs for all milestone-1 active domains.
- Add domain ADR links to roadmap Stage A review workflow.
- Revisit policy after milestone-1 Stage A completes.

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/overview/roadmap.md`

## References
- `docs/standards/adr.md`
- `docs/standards/data.md`
