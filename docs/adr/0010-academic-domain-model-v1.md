# ADR 0010: Academic Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The academic domain defines time structures (years, calendars, terms, days)
that scope instructional, enrollment, and reporting behavior.

## Decision

- `academic` owns canonical academic-time structures and related code tables.
- Calendars, events, days, and terms are separate first-class records.
- Downstream domains reference academic entities rather than duplicating term
  logic.

## Model and Field Breakdown

- Baseline field patterns:
  - year/calendar hierarchy
  - term typing with code table
  - event/day records for fine-grained schedule context

- `AcademicYear`
  - Required: `year_code`, `label`
  - Included: `organization_id`, `starts_on`, `ends_on`, `is_active`, `is_current`
- `AcademicCalendar`
  - Required: `academic_year_id`, `name`
  - Included: `organization_id`, `is_default`
- `AcademicTermTypeCode`
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
- `AcademicCalendarEvent`
  - Required: `calendar_id`, `title`, `starts_on`, `ends_on`
  - Included: `description`, `is_public`
- `AcademicCalendarDay`
  - Required: `calendar_id`, `calendar_date`
  - Included: `is_workday`, `is_instructional`, `is_holiday`, `metadata`
- `AcademicTerm`
  - Required: `academic_year_id`, `term_type_code_id`, `label`, `starts_on`, `ends_on`
  - Included: `calendar_id`, `parent_term_id`, `organization_id`, `code`

## Consequences

- Positive:
  - Consistent temporal scoping for instruction/enrollment/reporting.
  - Supports district-specific calendar complexity.
- Tradeoffs:
  - Calendar correctness is critical and can impact multiple domains.
  - Requires careful handling of overlapping terms/events edge cases.

## Alternatives Considered

- Keep academic timing in instruction domain only.
  - Rejected to avoid duplicated calendar semantics.
- Minimal year/term-only model.
  - Rejected to preserve day/event-level extensibility.

## Follow-Up

- Define canonical academic-year rollover/activation processes.
- Confirm event/day type taxonomy and validation rules.
- Define constraints for cross-calendar term references.

## Review Sign-off Checklist

- [ ] Academic-time ownership confirmed
- [ ] Calendar/term model confirmed
- [ ] Cross-domain academic reference policy confirmed
- [ ] Time-bound validation rules confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`
- Adjacent: `docs/adr/0011-instruction-domain-model-v1.md`, `docs/adr/0012-enrollment-domain-model-v1.md`

## References

- `services/inventory-backend/apps/academic/`
