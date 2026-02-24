# ADR 0014: Instruction Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering

## Context
Instruction is scaffolded and needs a clear baseline for course/section/schedule
entities that can integrate with academic and enrollment domains.

## Decision
1. Keep instructional catalog and schedule ownership in `instruction`.
2. Baseline entity set should include:
   `course`, `section`, `schedule`, and term-link relationships.
3. Keep academic window semantics in `academic`; instruction references those
   records rather than redefining time windows.
4. Keep enrollment relationships in `enrollment`; instruction should not own
   roster assignment rows.
5. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Current implemented models:
- No concrete Django models are implemented yet in `apps/instruction/models/`.

Planned baseline model set for Stage A review:
- `Course`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `course_code`, `title`, `description`, `organization_scope`
- `Section`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `course`, `academic_term`, `organization_scope`
  - Proposed domain fields: `section_code`, `label`, `starts_on`, `ends_on`
- `Schedule`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `section`
  - Proposed domain fields: `meeting_pattern`, `day_mask`, `start_time`, `end_time`, `room_ref`

## Domain Review Note
- Field list above for planned models is provisional until Stage A model review
  and migration design are complete.

## Consequences
- Preserves clean boundaries between instruction, academic, and enrollment.
- Enables incremental rollout of schedule complexity.
- Requires coordinated API design across related domains.

## Alternatives Considered
- Merge instruction and enrollment into one domain.
- Keep schedule metadata directly on enrollment entities.

## Follow-Up
- Draft initial instruction models and migration chain in milestone-1 Stage A.
- Define API exposure sequence for course/section/schedule resources.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0019-academic-time-model-v2.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `docs/overview/roadmap.md`
- `services/inventory-backend/apps/instruction/models/__init__.py`
