# ADR 0006: Identity Domain Model

- **Status**: Accepted
- **Date**: 2026-03-03
- **Owners**: Platform Team

## Context

The identity domain owns account identity, authentication-adjacent profile data,
role assignment links, and identity metadata used across all other domains.

## Decision

- `identity` is the system-of-record domain for users and persona identity.
- Identity is globally referenceable by other domains using stable identifiers.
- Role assignment relationships are owned by identity, while permission policy is
  defined by [ADR 0005](./0005-rbac-model-and-permission-enforcement.md).
- Identity stores account/persona detail and demographics data needed for
  product behavior and policy enforcement.
- Identity code tables should use canonical product-owned values first, even
  when downstream interoperability/reporting standards such as OneRoster or
  Texas TSDS/PEIMS need alternate codes.
- Authentication eligibility behavior is derived from:
  - active user status
  - active role assignment windows
  - user and role login lock windows

## Model and Field Breakdown

- Baseline field patterns:
  - internal PK + external `uuid`
  - audit fields from common base models
  - effective windows for assignment-style records

- `User`
  - Required: `email`
  - Included: `first_name`, `last_name`, `is_active`, `is_staff`, `require_password_reset`, `activated_at`, `inactivated_at`, `inactivated_by_id`, `verified_at`
- `Profile`
  - Required: `user_id`
  - Included: `preferred_name`, `display_name`, `slug`, `pronouns`, `headline`, `about`, `avatar_url`, `banner_url`
- `RoleAssignment`
  - Required: `user_id`, `role_id`, `starts_on`
  - Included: `ends_on`
- `RoleAssignmentOrganization`
  - Required: `role_assignment_id`, `organization_id`
  - Included: none
- `UserLoginLock` / `RoleLoginLock`
  - Required: `user_id|role_id`, `starts_at`
  - Included: `ends_at`, `reason`
- `UserAdditionalIdentifier`
  - Required: `user_id`, `system`, `identifier_type`, `identifier_value`
  - Included: none
- `PrefixCode` / `SuffixCode` / `GenderCode` / `RaceCode` / `EthnicityCode`
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
  - Seed baseline: canonical product-owned values are seeded through the
    identity domain management command and stored in per-model seed files under
    `services/inventory-backend/apps/identity/seeds/`
- `StudentDetail` / `StaffDetail` / `GuardianDetail`
  - Required: `user_id`
  - Included: `prefix_id`, `first_name`, `middle_name`, `last_name`, `suffix_id`, `date_of_birth`, `birth_country`, `birth_state`, `birth_city`, `local_id`
- `StudentDemographics` / `StaffDemographics` / `GuardianDemographics`
  - Required: `user_id`
  - Included: `gender_id`, `race_id`, `ethnicity_id`, demographic boolean flags

## Consequences

- Positive:
  - Clear ownership of account identity and role assignment lifecycle.
  - Consistent identity linking across domains.
- Tradeoffs:
  - Identity model changes can have broad downstream impact.
  - Requires strict migration discipline when changing core user structures.

## Alternatives Considered

- Split authentication and profile/demographics into separate domains.
  - Deferred to avoid early fragmentation and coordination overhead.
- Keep role assignment outside identity.
  - Rejected because assignment lifecycle is identity-centric.

## Follow-Up

- Swap identity placeholder fields `birth_country_id` and `birth_state_id` to
  real foreign keys when the locations domain model is implemented.
- Add `RoleAssignmentOrganization` when the organization domain model is
  established on the phase-1 organization branch.
- Add external code mapping support for identity code tables so canonical values
  can map to standards such as OneRoster and Texas TSDS/PEIMS without making
  the core identity tables jurisdiction-specific.
- Revisit whether external-code mappings should live on the code tables
  directly or in dedicated mapping tables once domain patterns across
  organization, locations, contacts, and academic are established.
- Decide whether later domains should follow the same per-model seed-file
  structure used by identity or whether a shared domain-level seed convention
  needs to be documented in standards.
- Finalize non-delegable/system-level permission boundaries tied to assignments.
- Confirm constraints for persona detail completeness by role/persona type.
- Define lifecycle rules for lock records and reactivation flow.

## Review Sign-off Checklist

- [x] Identity ownership boundaries confirmed
- [x] Role assignment lifecycle confirmed
- [x] Persona/demographics scope confirmed
- [x] Cross-domain identity linking rules confirmed

## Related ADRs

- Dependencies: [ADR 0004](./0004-domain-boundaries-and-ownership.md), [ADR 0005](./0005-rbac-model-and-permission-enforcement.md)
- Adjacent: [ADR 0007](./0007-organization-domain-model-v1.md)

## References

- `services/inventory-backend/apps/identity/`
