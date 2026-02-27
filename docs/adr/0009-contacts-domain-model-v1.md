# ADR 0009: Contacts Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The contacts domain owns communication endpoints and relationship records
between users/personas relevant to student and staff contexts.

## Decision

- `contacts` owns phone, email, and user-address association records.
- Contacts also owns person-to-person relationship models for student/guardian
  and staff relationship contexts.
- Contact methods use controlled code tables for type classification.

## Model and Field Breakdown

- Baseline field patterns:
  - contact method code tables + method records
  - explicit relationship records with lifecycle/audit attributes

- `PhoneCode` / `EmailCode`
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
- `Phone`
  - Required: `user_id`, `phone_number`, `phone_code_id`
  - Included: `extension`, `is_primary`, `is_sms_capable`, `is_sms_opted_out`, `sms_opted_out_at`, `sort_order`
- `Email`
  - Required: `user_id`, `email_address`, `email_code_id`
  - Included: `is_primary`, `is_notification_enabled`, `sort_order`
- `UserAddress`
  - Required: `user_id`, `address_id`, `address_type`
  - Included: `is_primary`, `source_system`, `source_record_id`, `starts_on`, `ends_on`
- `StudentRelationship`
  - Required: `student_id`, `related_student_id`
  - Included: `relationship_label`, `starts_on`, `ends_on`
- `StudentGuardianRelationship`
  - Required: `student_id`, `guardian_id`
  - Included: `relationship_label`, `is_primary_contact`, `starts_on`, `ends_on`
- `StaffAssignment`
  - Required: `staff_id`, `starts_on`
  - Included: `organization_id` xor `facility_id`, `ends_on`, `is_primary`

## Consequences

- Positive:
  - Centralized contact and relationship handling across workflows.
  - Supports authorization and notification logic based on relationships.
- Tradeoffs:
  - Relationship integrity rules must remain aligned with identity/persona data.
  - Potential overlap pressure with enrollment/instruction associations.

## Alternatives Considered

- Store contact methods directly on user/profile only.
  - Rejected to support multiple methods and typed/contact lifecycle handling.
- Put relationship models in enrollment.
  - Rejected because relationships extend beyond enrollment workflows.

## Follow-Up

- Define canonical uniqueness rules for phone/email records.
- Confirm relationship status/lifecycle semantics for guardianship changes.
- Define validation policy for contact method verification state.

## Review Sign-off Checklist

- [ ] Contact method ownership confirmed
- [ ] Relationship model ownership confirmed
- [ ] Code-table strategy confirmed
- [ ] Lifecycle and validation rules confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0006-identity-domain-model-v1.md`
- Adjacent: `docs/adr/0012-enrollment-domain-model-v1.md`

## References

- `services/inventory-backend/apps/contacts/`
