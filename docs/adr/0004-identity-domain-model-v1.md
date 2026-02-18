# ADR 0004: Identity Domain Model v1

- **Status**: Accepted
- **Date**: 2026-02-16
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
Identity modeling for MVP needs to support authentication, profile UX, and
persona-specific district data (student, staff, guardian) without overloading a
single user table. Early drafts mixed account, profile, and demographics
concerns and increased migration churn.

## Decision
1. Keep `identity.User` focused on account/authentication concerns:
   email login, password auth state, RBAC compatibility, and account lifecycle.
2. Keep `identity.Profile` lightweight and UI-facing:
   social-style presentation fields (display/preferred naming, pronouns,
   slug handle, headline/about, avatar/banner) only.
3. Split persona-specific basic person fields into separate models:
   `StudentDetail`, `StaffDetail`, and `GuardianDetail`.
   Include core naming fields plus code-table-backed `prefix`, `suffix`,
   birth country/state via shared `contacts` code tables, and free-text `birth_city`.
4. Use shared audit attribution fields (`created_by`, `updated_by`) through
   common abstract models.
5. Keep lifecycle fields (`activated_at`, `inactivated_at`, `inactivated_by`)
   on `identity.User`, not as global common fields.
6. Keep historical tracking enabled for identity entities with explicit
   exclusion of sensitive/high-noise fields.
7. Enforce role-based access using time-windowed role assignments
   (`starts_on`, `ends_on`) so account access can expire by role window even
   when the account record remains active.
8. Standardize identifiers on identity entities:
   internal DB primary key is `id` (`BigAutoField`), external stable identifier
   is `uuid` (`UUIDField`, unique, indexed).
9. Lock `identity.User` historical tracking scope for MVP:
   include all business and lifecycle fields, exclude `password`, `last_login`,
   `created_at`, and `updated_at`.
10. Allow one role assignment to scope across multiple organizations using
    a related scope table (`RoleAssignmentOrganization`) keyed by a direct
    foreign key to `organization.Organization` (many scopes to one organization).
11. Keep demographic models focused on demographic payloads and move
    external/source identifier mapping to `UserAdditionalIdentifier`
    (`system`, `identifier_type`, `identifier_value`).
12. Keep additional email endpoints in `contacts` via `Email`
    and `EmailCode` instead of storing secondary email on persona detail rows.
13. Keep `is_active` on `identity.User` as the hard account-authentication gate.
14. Keep `require_password_reset` on `identity.User` so administrators can
    force a password change at next successful login.
15. Implement temporary operational login lockouts as dedicated models:
    `UserLoginLock` and `RoleLoginLock`.
    Lockouts are separate from role assignment windows.
16. Keep `gender`, `race`, and `ethnicity` as code-table-backed demographic
    fields on persona demographics models, not detail models.

## Locked Identity User v1

### `identity_user` (source of truth)
- Identity: `id`, `uuid`, `email`
- Person label fields: `first_name`, `last_name`
- Access/state: `is_active`, `is_staff`, `is_superuser`
- Lifecycle: `activated_at`, `inactivated_at`, `inactivated_by`, `verified_at`
- Audit attribution: `created_by`, `updated_by`
- Django auth relationships: `groups`, `user_permissions`

### `identity_historicaluser` (simple history)
- Tracks: `id`, `uuid`, `email`, `first_name`, `last_name`, `is_active`,
  `is_staff`, `is_superuser`, `activated_at`, `inactivated_at`, `inactivated_by`,
  `verified_at`, `created_by`, `updated_by`, plus history metadata fields.
- Excludes: `password`, `last_login`, `created_at`, `updated_at`.

## Consequences
- Reduces schema coupling and keeps account logic stable.
- Improves UI clarity by isolating profile from operational demographics.
- Supports future role/persona evolution with additive changes.
- Requires additional joins for persona-heavy views.

## Alternatives Considered
- Single wide user table for account/profile/demographics.
- User + profile only, with one shared demographics table for all personas.
- Lifecycle fields on every domain table by default.

## Follow-Up
- Add migration split strategy after baseline stabilizes.
- Add API/serializer boundaries so default user endpoints stay minimal.

## Related
- `docs/adr/0001-auth-strategy.md`
- `docs/adr/0002-core-data-model.md`
- `docs/overview/roadmap.md`
- `docs/standards/data.md`

## References
- `docs/overview/feature-candidates.md`
