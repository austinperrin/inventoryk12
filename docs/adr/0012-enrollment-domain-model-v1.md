# ADR 0012: Enrollment Domain Model

- **Status**: Accepted
- **Date**: 2026-03-06
- **Owners**: Platform Team

## Context

The enrollment domain needs a SIS-aligned structure for:
- student placement at campus + grade level over time
- student section membership windows
- staff section membership windows

The model also needs to align with access policy where student access depends
on active enrollment lifecycle.

## Decision

- `enrollment` owns:
  - `StudentEnrollment` (student-to-organization + grade-level lifecycle)
  - `StudentSchedule` (student-to-section lifecycle)
  - `StaffSchedule` (staff-to-section lifecycle)
- Enrollment references instruction entities (`Section`) and identity entities
  (`User`, role-assignment records) without duplicating instructional structure.
- Enrollment is source-of-truth for student academic lifecycle windows.
- Identity student role-assignment lifecycle is derived from enrollment data by
  sync rules, not separate manual entry.
- Entry/exit semantics are optional in v1 and captured with nullable code-table
  references.
- Enrollment does not own contact relationships, courses, sections, periods, or
  meeting patterns.

## Model and Field Breakdown

- `EnrollmentEntryCode` / `EnrollmentExitCode` (planned)
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`,
    `is_active`

- `StudentEnrollment`
  - Required: `student_user_id`, `organization_id`, `grade_level_code_id`,
    `starts_on`
  - Included: `ends_on`, `entry_code_id` (nullable),
    `exit_code_id` (nullable), `notes`,
    `source_system`, `source_record_id`, `role_assignment_id` (audit link),
    `role_assignment_org_id` (audit link)

- `StudentSchedule`
  - Required: `section_id`, `student_user_id`, `starts_on`
  - Included: `ends_on`, `entry_code_id` (nullable),
    `exit_code_id` (nullable), `notes`,
    `source_system`, `source_record_id`

- `StaffSchedule`
  - Required: `section_id`, `staff_user_id`, `starts_on`
  - Included: `ends_on`, `staff_assignment_role_code_id`, `is_primary`,
    `notes`, `source_system`, `source_record_id`

## Expected Constraints (Planned)

- Date-window checks enforce `ends_on >= starts_on`.
- No overlapping active `StudentEnrollment` windows for the same student +
  organization.
- No overlapping active `StudentSchedule` rows for the same student + section.
- No overlapping active `StaffSchedule` rows for the same staff + section.
- `StudentSchedule` and `StaffSchedule` windows must fit section windows when
  section dates are present.
- Enrollment/schedule state is inferred from lifecycle windows and section
  window context (for example, active, withdrawn, completed).
- Student access eligibility requires an active student role assignment and
  active `StudentEnrollment` window; effective access is the intersection.
- For student personas, role-assignment lifecycle is synchronized from
  `StudentEnrollment` changes (create/update/end) and is not manually managed.
- Do not enforce single-primary-teacher uniqueness at DB level in v1.

## Consequences

- Positive:
  - Clean split between instructional structure and membership lifecycle.
  - Supports SIS-like campus placement + section membership patterns.
  - Prevents duplicate manual lifecycle input by deriving student role windows
    from enrollment.
  - Keeps v1 enrollment model minimal by deriving state from date windows.
  - Preserves structured entry/exit details while keeping them optional.
- Tradeoffs:
  - Requires robust sync/reconciliation between enrollment and identity role
    assignments.
  - Cross-domain dependencies remain high (identity, instruction, organization,
    academic).
  - Historical change intent is less explicit without a dedicated event stream.

## Alternatives Considered

- Use role assignment as the only source-of-truth for student lifecycle.
  - Rejected because academic placement fields (grade, enrollment entry/exit)
    do not belong in IAM models.
- Use only one schedule table for student + staff.
  - Rejected to avoid mixed constraints and persona-specific rule sprawl.
- Keep enrollment inside instruction models.
  - Rejected to preserve lifecycle-focused ownership and cleaner boundaries.

## Follow-Up

- Define inferred-state rules in one canonical service policy so all consumers
  interpret lifecycle windows consistently.
- Define baseline entry/exit code seeds and keep `entry_code_id` /
  `exit_code_id` nullable in v1.
- Define service-level sync contract from `StudentEnrollment` to identity
  student role assignment windows (including repair/reconciliation flow).
- Define conflict-resolution behavior for imported SIS records with overlapping
  windows.
- Define guardianship/parent visibility joins to schedule/enrollment records.
- Decide whether enrollment event/audit stream is needed in a later milestone
  if operational support/audit demands increase.
- Confirm whether `StaffSchedule.is_primary` remains informational in v1 or
  gains policy-level restrictions later.

## Review Sign-off Checklist

- [ ] Enrollment ownership boundaries confirmed
- [ ] StudentEnrollment + StudentSchedule + StaffSchedule scope confirmed
- [ ] Lifecycle-derived state rules confirmed
- [ ] Enrollment-driven role-assignment sync rules confirmed
- [ ] Cross-domain reference rules confirmed
- [ ] Historical audit policy confirmed

## Related ADRs

- Dependencies: [ADR 0004](./0004-domain-boundaries-and-ownership.md), [ADR 0006](./0006-identity-domain-model-v1.md), [ADR 0011](./0011-instruction-domain-model-v1.md)
- Adjacent: [ADR 0009](./0009-contacts-domain-model-v1.md), [ADR 0010](./0010-academic-domain-model-v1.md)

## References

- `services/inventory-backend/apps/enrollment/`
