# ADR 0011: Instruction Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The instruction domain will own instructional structures such as courses,
sections/classes, schedules, and instructional metadata.

## Decision

- `instruction` owns instructional structure records and scheduling metadata.
- Instruction references `academic` for time context and `organization` for
  scope context.
- Enrollment membership records are owned by `enrollment`, not `instruction`.

## Model and Field Breakdown

- `Course` (planned)
  - Required: `organization_id`, `course_code`, `title`
  - Included: `description`, `subject_code`, `grade_band`, `is_active`
- `Section` (planned)
  - Required: `course_id`, `section_code`, `academic_term_id`
  - Included: `organization_id`, `facility_id`, `staff_user_id`, `capacity`, `starts_on`, `ends_on`, `is_active`
- `SectionMeetingPattern` (planned)
  - Required: `section_id`, `day_of_week`, `starts_at`, `ends_at`
  - Included: `room_label`, `notes`

## Expected Constraints (Planned)

- Date windows use `starts_on <= ends_on` and `starts_at < ends_at` checks.
- Section uniqueness is enforced per organization and term (for example, unique
  on `organization_id`, `academic_term_id`, `section_code`).
- `staff_user_id` and `facility_id` are optional links but must reference active
  records when present.

## Consequences

- Positive:
  - Separates instructional structure from roster membership concerns.
  - Supports SIS-aligned modeling for section-level operations.
- Tradeoffs:
  - Requires clear contract with enrollment domain for roster ownership.
  - Model design must balance flexibility vs schema complexity.

## Alternatives Considered

- Collapse instruction and enrollment into one domain.
  - Rejected to preserve cleaner boundaries and lifecycle handling.
- Put instruction under academic domain.
  - Rejected due to distinct ownership and behavior patterns.

## Follow-Up

- Define core instruction entities and identifiers.
- Define schedule model scope (meeting patterns vs simple period references).
- Define integration mapping requirements for SIS data sources.

## Review Sign-off Checklist

- [ ] Instruction ownership boundaries confirmed
- [ ] Core entity set confirmed
- [ ] Instruction-enrollment contract confirmed
- [ ] Academic/organization reference rules confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0007-organization-domain-model-v1.md`, `docs/adr/0010-academic-domain-model-v1.md`
- Adjacent: `docs/adr/0012-enrollment-domain-model-v1.md`

## References

- `services/inventory-backend/apps/instruction/`
