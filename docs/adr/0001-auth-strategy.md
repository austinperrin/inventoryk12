# ADR 0001: Authentication Strategy

## Title
Authentication Strategy

## Status
Accepted (2026-02-10)

## Context
InventoryK12 requires role-based access for district staff, students, and
parents/guardians, with a long-term requirement for SSO and MFA. The MVP must
support a district pilot with minimal integration burden while remaining
compatible with future SSO and external add-on integrations.

## Decision
Proposed approach:
- MVP uses per-product authentication within InventoryK12.
- Login uses email/password for MVP.
- MFA is optional (user opt-in) for MVP.
- User provisioning supports manual creation in the UI.
- User provisioning supports automated imports (CSV via SFTP, OneRoster).
- User provisioning supports manual CSV upload in the UI.
- Password policy follows default Django password requirements for MVP.
- SSO/MFA support is a Phase 2/3 milestone (OneRoster, LDAP/Azure Entra).
- Portal access is role-based with a shared UI; future portal-specific login
  policies are supported via configuration.

## Consequences
- Faster MVP delivery without requiring district SSO upfront.
- Requires a migration plan when SSO becomes mandatory for larger districts.
- Impacts UI flows for login, user management, and role assignment.

## Alternatives Considered
- Per-product auth only with no SSO roadmap.
- Immediate SSO-first approach (higher complexity, slower MVP).
- Shared auth service as a separate integration service (adds infra earlier).

## References
- `docs/standards/security.md`
