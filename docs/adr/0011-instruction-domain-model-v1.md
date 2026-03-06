# ADR 0011: Instruction Domain Model

- **Status**: Accepted
- **Date**: 2026-03-06
- **Owners**: Platform Team

## Context

Instruction needs a SIS-aligned structure for course catalog, class sections,
and reusable time blocks. The initial outline was too small for later
attendance/gradebook/scheduling use cases, and we need explicit boundaries with
enrollment before implementation begins.

## Decision

- `instruction` owns instructional structure and schedule primitives:
  - course catalog
  - section/class definition
  - period definitions
  - section meeting patterns
- Instruction references `academic` for term/year context, `organization` for
  ownership scope, and `locations` for facility/room context.
- Instruction does not own student/staff membership in sections. Membership is
  owned by `enrollment`.
- `CourseOffering` is intentionally out of v1 scope. Term scoping is handled on
  `Section` directly and can be normalized later if needed.

## Model and Field Breakdown

- Baseline field patterns:
  - internal PK + external `uuid`
  - shared audit/history fields
  - effective window dates where applicable
  - instruction-owned code tables for typed instructional values

- `Course` (catalog)
  - Required: `organization_id`, `course_code`, `title`
  - Included: `description`, `subject_code_id`, `grade_low_code_id`,
    `grade_high_code_id`, `is_active`

- `CourseAdditionalIdentifier`
  - Required: `course_id`, `system`, `identifier_type`, `identifier_value`
  - Included: `starts_on`, `ends_on`

- `Section` (class instance)
  - Required: `course_id`, `organization_id`, `academic_term_id`,
    `section_code`
  - Included: `starts_on`, `ends_on`

- `SectionAdditionalIdentifier`
  - Required: `section_id`, `system`, `identifier_type`, `identifier_value`
  - Included: `starts_on`, `ends_on`

- `Period` (org/facility time block)
  - Required: `organization_id`, `period_code`, `label`, `starts_at`, `ends_at`
  - Included: `facility_id`, `sort_order`, `is_active`

- `SectionMeetingPattern`
  - Required: `section_id`, `day_of_week`, `starts_at`, `ends_at`
  - Included: `period_id`, `location_facility_id`, `cycle_day`,
    `starts_on`, `ends_on`, `notes`

- Code tables (planned):
  - `SubjectCode`
  - `GradeLevelCode` (shared by instruction/enrollment usage)

## Expected Constraints (Planned)

- `starts_on <= ends_on` and `starts_at < ends_at` checks are enforced.
- `Course.course_code` is unique per organization.
- `Section.section_code` is unique per organization + academic term.
- `Period.period_code` is unique per organization.
- Section activity is derived from the section lifecycle window (`starts_on`,
  `ends_on`) rather than a separate status/type table in v1.
- `CourseAdditionalIdentifier` is unique per course + system + identifier_type +
  identifier_value.
- `SectionAdditionalIdentifier` is unique per section + system +
  identifier_type + identifier_value.
- Additional identifier rows enforce `starts_on <= ends_on` when both values are
  set.
- `Section` window must fit inside referenced academic term window when section
  dates are set.
- `SectionMeetingPattern` window must fit inside section window when meeting
  dates are set.
- Section location is sourced from `SectionMeetingPattern.location_facility_id`
  and inferred through the facility parent chain, not stored directly on
  `Section`.
- `location_facility_id` must point to a schedulable facility node type
  (for example, room/lab/field according to district policy).
- The referenced facility must have a valid ancestor chain for reporting scope
  (for example room -> building -> school) based on configured facility-code
  rules.
- A section may exist in draft/unscheduled state with zero meeting patterns,
  but must have at least one meeting pattern before it is considered
  schedulable.
- `Period` overlap policy within an organization is explicitly defined and
  validated (allow overlap by design if district policy requires it, otherwise
  prohibit).

## Consequences

- Positive:
  - Keeps instructional structure independent from membership lifecycle.
  - Supports SIS-like course/section/period scheduling patterns.
  - Leaves room for future normalization (`CourseOffering`) without blocking M2.
- Tradeoffs:
  - More code-table and validation surface area than a minimal section model.
  - Requires careful coordination with enrollment for schedule membership rules.

## Alternatives Considered

- Add `CourseOffering` in v1.
  - Deferred to keep M2 implementation smaller and faster.
- Store student/staff membership inside instruction.
  - Rejected; membership lifecycle belongs to enrollment.
- Put instruction under academic domain.
  - Rejected; academic owns time primitives, not instructional entities.

## Follow-Up

- Finalize initial seed sets for instruction code tables.
- Keep code-table scope minimal in v1 (`SubjectCode`, `GradeLevelCode` only).
- Defer `CourseLevelCode`, `CreditTypeCode`, `SectionStatusCode`, and
  `PeriodTypeCode` unless concrete workflow requirements are identified.
- Defer course credit tracking fields (`credits_attempted`,
  `credits_earned_default`) to a later ADR/workstream.
- Defer bell schedule modeling to a later ADR with a structure such as:
  `BellSchedule` (org/facility + date window), `BellScheduleGradeBand`
  (schedule + grade level), and `BellSchedulePeriod` (schedule + period +
  period-type semantics). This supports campus/grade-specific period meaning
  (for example, period 1 as homeroom for one grade and passing for another).
- Confirm locations-domain facility-code rules for schedulable node types and
  required ancestor-chain validation used by
  `SectionMeetingPattern.location_facility_id`.
- Decide whether `GradeLevelCode` is owned in instruction or moved to a shared
  academic/enrollment location in a later ADR.
- Document period overlap policy default for districts.
- Define OneRoster/SIS mapping for `course`, `class/section`, and period/bell
  schedule exports.
- Revisit `CourseOffering` only if section-level duplication becomes a real
  operational issue.

## Review Sign-off Checklist

- [ ] Instruction ownership boundaries confirmed
- [ ] Course/Section/Period v1 scope confirmed
- [ ] Instruction-enrollment contract confirmed
- [ ] Academic/organization/locations reference rules confirmed

## Related ADRs

- Dependencies: [ADR 0004](./0004-domain-boundaries-and-ownership.md), [ADR 0007](./0007-organization-domain-model-v1.md), [ADR 0010](./0010-academic-domain-model-v1.md)
- Adjacent: [ADR 0012](./0012-enrollment-domain-model-v1.md)

## References

- `services/inventory-backend/apps/instruction/`
