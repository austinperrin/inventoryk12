# ADR 0005: RBAC Model and Permission Enforcement

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

This ADR defines the role and permission model for API and application access
control.

## Decision

- RBAC baseline uses Django Groups + Permissions as the core authorization
  model.
- Deployment scope is single-district per stack, so role scopes are
  environment-local and not multi-tenant within one runtime.
- System-managed seeded roles are created during onboarding and protected from
  deletion.
- District-managed custom roles are allowed and implemented as additional
  groups with bounded admin controls.
- Delegated administration is allowed:
  - users with designated admin roles can assign approved roles/permissions to
    other users
  - delegated assignment is bounded by role/permission guardrails
  - users cannot grant permissions above their own delegated authority
- Role assignment windows are time-bound capable (effective start/end) using
  identity domain assignment models.
- Enforcement baseline:
  - DRF endpoints with sensitive operations must enforce explicit permission
    checks.
  - Authorization logic should live in dedicated permission classes/policies,
    not inline view logic.
  - Default is deny unless explicitly allowed.
- External role mapping (for example OneRoster) maps into seeded/custom role
  model with least-privilege fallback for unknown roles.
- Non-prod environment baseline:
  - sandbox/training role configuration is cloned from prod by default
  - per-environment role divergence is a later-phase option

## Model and Field Breakdown

- Identity domain model alignment:
  - users and profile models carry account identity
  - role assignment models carry role-to-user relationships and effective
    windows
  - login lock and auth detail models support account security controls
- Authorization control points:
  - API permission classes
  - service-layer policy checks for non-HTTP execution paths (jobs/tasks)
  - admin/back-office tooling role checks
- Baseline capability matrix:

| Role | Assign Roles/Permissions | Manage Users | Manage Assets | Run Imports | Run Audits | View Reports |
| --- | --- | --- | --- | --- | --- | --- |
| district_admin | Yes (bounded) | Yes | Yes | Yes | Yes | Yes |
| site_admin | Yes (bounded) | Limited | Yes | Yes | Yes | Yes |
| system_admin | Yes (bounded) | Limited | Yes | Yes | Yes | Yes |
| principal | No | Limited | Yes | Yes | Yes | Yes |
| teacher | No | No | Limited | No | No | Limited |
| counselor | No | No | Limited | No | No | Limited |
| aide | No | No | Limited | No | No | Limited |
| proctor | No | No | No | No | No | Limited |
| student | No | No | No | No | No | Limited |
| parent | No | No | No | No | No | Limited |
| guardian | No | No | No | No | No | Limited |
| relative | No | No | No | No | No | Limited |

Notes:
- "bounded" means delegation is constrained by non-delegable/system-level
  permissions and policy checks.
- "Limited" means scoped by campus/org and often read-only depending on
  capability.

## Consequences

- Positive:
  - Uses mature Django-native authorization primitives.
  - Supports controlled extensibility for district-specific needs.
  - Aligns with principle of least privilege.
- Tradeoffs:
  - Group/permission sprawl risk without governance.
  - Requires clear auditability for role grants and revocations.

## Alternatives Considered

- Hard-coded role checks only (no permission model).
  - Rejected due to maintainability and poor extensibility.
- Fully custom policy engine from day one.
  - Deferred due to implementation complexity and limited early-stage benefit.
- ABAC-only model in v1.
  - Deferred; can be layered later for fine-grained conditional access.

## Follow-Up

- Define and document seed-role permission matrix by product capability.
- Define district custom-role guardrails (restricted permission sets).
- Define RBAC audit trail requirements for role grants/revocations.
- Define support/admin break-glass workflow and logging requirements.
- Open questions:
  - Finalize the non-delegable permission set and assignment guardrails.
  - Do parent/guardian roles require object-level access constraints tied to
    student relationships at launch?
  - Future phase: should sandbox/training support explicit per-environment role
    divergence?

## Review Sign-off Checklist

- [ ] Seed-role model confirmed
- [ ] Custom-role policy confirmed
- [ ] API enforcement baseline confirmed
- [ ] Role assignment lifecycle policy confirmed

## Related

- `docs/standards/security.md`
- `docs/adr/0002-url-and-domain-topology.md`
- `docs/adr/0003-non-prod-data-refresh-and-sanitization-policy.md`
- `docs/adr/0006-identity-domain-model-v1.md`

## References

- `services/inventory-backend/apps/identity/`
