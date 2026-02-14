# ADR 0001: Authentication Strategy

- **Status**: Accepted
- **Date**: 2026-02-13
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
InventoryK12 requires role-based access for district staff, students, and
parents/guardians, with a long-term requirement for SSO and MFA. The MVP must
support a district pilot with minimal integration burden while remaining
compatible with future SSO and external add-on integrations.

## Decision
1. **MVP authentication baseline**: InventoryK12 uses product-local authentication
   for MVP, with email/password login and role-based access control.
2. **MFA approach for MVP**: MFA is optional (user opt-in) during MVP. Tenant-level
   mandatory MFA is deferred to later milestones.
3. **Provisioning baseline**: Provisioning supports manual user creation in the UI,
   manual CSV upload, and automated import flows (CSV via SFTP, OneRoster).
4. **Policy baseline**: Password policy follows default Django requirements for MVP.
5. **Future integration direction**: SSO/MFA integration (including OneRoster and
   LDAP/Azure Entra) is planned for Milestone 2/3.
6. **Portal model**: Portal access remains role-based with a shared UI, while
   portal-specific login policies remain a future configurable extension.

## Consequences
- Faster MVP delivery without requiring district SSO upfront.
- Requires a migration plan when SSO becomes mandatory for larger districts.
- Impacts UI flows for login, user management, and role assignment.

## Alternatives Considered
- Per-product auth only with no SSO roadmap.
- Immediate SSO-first approach (higher complexity, slower MVP).
- Shared auth service as a separate integration service (adds infra earlier).

## Follow-Up
- Define and document SSO/MFA transition plan before Milestone 1 completion.
- Define JWT claim schema and token lifecycle controls.

## Related
- `docs/overview/roadmap.md` (Milestone 1 and Milestone 2 auth-related tasks)
- `docs/overview/inventoryk12-blueprint.md` (target users and role model)

## References
- `docs/standards/security.md`
