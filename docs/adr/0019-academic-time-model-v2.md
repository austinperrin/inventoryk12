# ADR 0019: Academic Time Model v2

- **Status**: Proposed
- **Date**: 2026-02-23
- **Owners**: Architecture, Backend Engineering, Data + Integrations

## Context
Academic-time modeling now includes explicit year/calendar/day/event/term type
entities with validation rules. The v1 ADR should be superseded by a detailed
v2 model and field breakdown aligned to the implemented schema.

## Decision
1. Keep academic-year, calendar, day, event, and term entities as first-class
   models in the `academic` domain.
2. Keep time-window semantics standardized with `starts_on`/`ends_on`.
3. Keep term typing explicit via `AcademicTermTypeCode`.
4. Keep relationship validation rules in-model for year/calendar/term coherence.
5. Preserve identifier contract:
   internal key is `id` (`BigAutoField`), external identifier is `uuid`.

## Model and Field Breakdown
Shared inherited fields for all models in this ADR:
- `id` (internal primary key, `BigAutoField`)
- `uuid` (external identifier, `UUIDField`)
- `created_at`, `updated_at`
- `created_by`, `updated_by`

`AcademicYear`:
- `year_code`, `label`
- `organization_id` (UUID, nullable)
- `starts_on`, `ends_on`
- `is_active`, `is_current`

`AcademicCalendar`:
- `academic_year` (FK)
- `organization_id` (UUID, nullable)
- `name`, `is_default`

`AcademicTermTypeCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`AcademicCalendarEvent`:
- `calendar` (FK)
- `title`, `description`
- `starts_on`, `ends_on`
- `is_public`

`AcademicCalendarDay`:
- `calendar` (FK)
- `calendar_date`
- `is_workday`, `is_instructional`, `is_holiday`
- `metadata` (JSON)

`AcademicTerm`:
- `academic_year` (FK)
- `calendar` (FK, nullable)
- `parent_term` (self FK, nullable)
- `organization_id` (UUID, nullable)
- `term_type_code` (FK)
- `code`, `label`
- `starts_on`, `ends_on`

## Consequences
- Captures current academic schema decisions in one canonical ADR.
- Improves cross-domain alignment for enrollment/instruction planning.
- Requires follow-up governance for rollover and year transition workflows.

## Alternatives Considered
- Keep ADR 0007 as active and append updates.
- Defer detailed model inventory until post-MVP.

## Follow-Up
- Add academic rollover workflow ADR (close/open year lifecycle operations).
- Add API contract ADR for year/calendar/term endpoints and edit permissions.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0007-academic-time-model-v1.md` (deprecated by this ADR)
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`
- `docs/overview/roadmap.md`

## References
- `services/inventory-backend/apps/academic/models/academic_time.py`
- `docs/adr/0003-ingestion-architecture.md`

