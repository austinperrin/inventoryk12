# ADR 0013: Enrollment Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering

## Context
Enrollment is currently scaffolded and should remain focused on instructional
enrollment windows and roster relationships without absorbing contact or
identity profile responsibilities.

## Decision
1. Keep enrollment scope limited to instructional enrollment/roster entities.
2. Model enrollment windows with `starts_on`/`ends_on` semantics.
3. Reference identity, organization, instruction, and academic records instead
   of duplicating their attributes.
4. Keep relationship ownership clear:
   guardian/student/staff relationship links stay in `contacts`.
5. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Current implemented models:
- No concrete Django models are implemented yet in `apps/enrollment/models/`.

Planned baseline model set for Stage A review:
- `UserEnrollment`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `user`, `section` or `instructional_entity`,
    `organization_scope`
  - Proposed lifecycle fields: `starts_on`, `ends_on`, `status_code`
  - Proposed source mapping fields: `source_system`, `source_record_id`

## Domain Review Note
- Field list above for planned models is provisional until Stage A model review
  and migration design are complete.

## Consequences
- Reduces overlap with identity and contacts.
- Makes OneRoster-aligned mapping easier as integrations mature.
- Defers richer enrollment workflows until schema baseline is approved.

## Alternatives Considered
- Store broad person relationship data in enrollment.
- Treat enrollment as a generic cross-domain relationship store.

## Follow-Up
- Draft concrete table set (`user_enrollment`, roster windows, status codes).
- Add enrollment API and import contract ADR after baseline review.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `docs/overview/roadmap.md`
- `services/inventory-backend/apps/enrollment/models/__init__.py`
