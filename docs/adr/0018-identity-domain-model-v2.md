# ADR 0018: Identity Domain Model v2

- **Status**: Proposed
- **Date**: 2026-02-23
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
Identity modeling has evolved beyond the original v1 scope and now includes
additional login lock, role-scope, demographics, and identifier entities.
The v1 ADR should be superseded by a full model and field inventory aligned to
the current codebase and domain-review workflow.

## Decision
1. Keep `identity.User` focused on account/authentication state and lifecycle.
2. Keep profile, persona details, demographics, role scopes, additional
   identifiers, and lockout controls as separate bounded entities.
3. Keep code-table driven domain values for prefix/suffix/gender/race/ethnicity.
4. Keep role assignment windows (`starts_on`, `ends_on`) and separate login
   lock windows (`starts_at`, `ends_at`) for operational control.
5. Preserve identifier contract:
   internal key is `id` (`BigAutoField`), external identifier is `uuid`.

## Model and Field Breakdown
Shared inherited fields for all models in this ADR:
- `id` (internal primary key, `BigAutoField`)
- `uuid` (external identifier, `UUIDField`)
- `created_at`, `updated_at`
- `created_by`, `updated_by`

`User`:
- Identity/account: `email`, `first_name`, `last_name`
- Access/state: `is_active`, `is_staff`, `is_superuser`, `require_password_reset`
- Lifecycle: `activated_at`, `inactivated_at`, `inactivated_by`, `verified_at`
- Auth relations: `groups`, `user_permissions`

`Profile`:
- `user` (one-to-one FK)
- `preferred_name`, `display_name`, `slug`, `pronouns`, `headline`, `about`
- `avatar_url`, `banner_url`

`PrefixCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`SuffixCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`StudentDetail`:
- `user` (one-to-one FK)
- Persona fields: `prefix`, `first_name`, `middle_name`, `last_name`, `suffix`
- Birth fields: `date_of_birth`, `birth_country`, `birth_state`, `birth_city`
- `local_id`

`StaffDetail`:
- `user` (one-to-one FK)
- Persona fields: `prefix`, `first_name`, `middle_name`, `last_name`, `suffix`
- Birth fields: `date_of_birth`, `birth_country`, `birth_state`, `birth_city`
- `local_id`

`GuardianDetail`:
- `user` (one-to-one FK)
- Persona fields: `prefix`, `first_name`, `middle_name`, `last_name`, `suffix`
- Birth fields: `date_of_birth`, `birth_country`, `birth_state`, `birth_city`
- `local_id`

`GenderCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`RaceCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`EthnicityCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`StudentDemographics`:
- `user` (one-to-one FK)
- `gender`, `race`, `ethnicity` (FKs)
- Flags: `is_native`, `is_asian`, `is_african_american`, `is_hawaiian`, `is_white`

`StaffDemographics`:
- `user` (one-to-one FK)
- `gender`, `race`, `ethnicity` (FKs)
- Flags: `is_native`, `is_asian`, `is_african_american`, `is_hawaiian`, `is_white`

`GuardianDemographics`:
- `user` (one-to-one FK)
- `gender`, `race`, `ethnicity` (FKs)
- Flags: `is_native`, `is_asian`, `is_african_american`, `is_hawaiian`, `is_white`

`RoleAssignment`:
- `user` (FK), `role` (FK to `auth.Group`)
- `starts_on`, `ends_on`

`RoleAssignmentOrganization`:
- `role_assignment` (FK), `organization` (FK)

`UserAdditionalIdentifier`:
- `user` (FK)
- `system`, `identifier_type`, `identifier_value`

`UserLoginLock`:
- `user` (FK)
- `starts_at`, `ends_at`, `reason`

`RoleLoginLock`:
- `role` (FK to `auth.Group`)
- `starts_at`, `ends_at`, `reason`

## Consequences
- Provides one accurate source for current identity model scope.
- Reduces drift between roadmap review gates and implemented schema.
- Increases ADR maintenance as identity entities evolve.

## Alternatives Considered
- Keep ADR 0004 as active and append piecemeal notes.
- Split identity into multiple ADRs before completing v2 baseline.

## Follow-Up
- Add identity API contract ADR for payload shape and field exposure policy.
- Re-evaluate demographic payload structure after first workflow slices.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0004-identity-domain-model-v1.md` (deprecated by this ADR)
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`
- `docs/overview/roadmap.md`

## References
- `services/inventory-backend/apps/identity/models/user.py`
- `services/inventory-backend/apps/identity/models/profile.py`
- `services/inventory-backend/apps/identity/models/details.py`
- `services/inventory-backend/apps/identity/models/demographics.py`
- `services/inventory-backend/apps/identity/models/role_assignment.py`
- `services/inventory-backend/apps/identity/models/user_additional_identifier.py`
- `services/inventory-backend/apps/identity/models/login_lock.py`

