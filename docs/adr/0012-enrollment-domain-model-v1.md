# ADR 0012: Enrollment Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The enrollment domain will own membership relationships between users/personas
and instructional offerings over effective time windows.

## Decision

- `enrollment` owns roster membership records and enrollment lifecycle windows.
- Enrollment references instruction entities and identity/persona entities.
- Enrollment does not own contact relationships or instructional structure.

## Model and Field Breakdown

- `EnrollmentStatusCode` (planned)
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
- `SectionEnrollment` (planned)
  - Required: `section_id`, `student_user_id`, `status_code_id`, `starts_on`
  - Included: `ends_on`, `source_system`, `source_record_id`, `notes`
- `EnrollmentEvent` (planned)
  - Required: `section_enrollment_id`, `event_type`, `event_at`
  - Included: `actor_user_id`, `reason`, `metadata`

## Expected Constraints (Planned)

- Date window checks enforce `ends_on >= starts_on`.
- Overlapping active enrollment windows for the same student and section are not
  allowed.
- Enrollment history is append-oriented, and state transitions are recorded via
  `EnrollmentEvent`.

## Consequences

- Positive:
  - Clear ownership of roster history and enrollment transitions.
  - Supports auditability for membership changes over time.
- Tradeoffs:
  - Requires high-integrity sync behavior with SIS integrations.
  - Cross-domain dependencies are significant (identity, instruction, academic).

## Alternatives Considered

- Keep enrollment inside instruction models.
  - Rejected to preserve lifecycle-focused ownership and scalability.
- Store enrollment state directly on user profile.
  - Rejected for poor historical modeling and multi-class support.

## Follow-Up

- Define enrollment status taxonomy and transitions.
- Define conflict rules for overlapping enrollments.
- Define guardianship/parent visibility joins to enrollment records.

## Review Sign-off Checklist

- [ ] Enrollment ownership boundaries confirmed
- [ ] Lifecycle/status model confirmed
- [ ] Cross-domain reference rules confirmed
- [ ] Historical audit policy confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0006-identity-domain-model-v1.md`, `docs/adr/0011-instruction-domain-model-v1.md`
- Adjacent: `docs/adr/0009-contacts-domain-model-v1.md`, `docs/adr/0010-academic-domain-model-v1.md`

## References

- `services/inventory-backend/apps/enrollment/`
