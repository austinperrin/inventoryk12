# Access Control Standards

## Purpose

Define repo-wide access-control enforcement and validation expectations.

## Effective Permission Resolution

- Effective permissions are the cumulative union of:
  - active role assignments linked to Django Groups
  - direct user permissions on the user record
- Resolution is evaluated:
  - at login/session establishment for access outcome
  - at request time for protected endpoint authorization
- Users with zero effective permissions are routed to a dedicated no-access or
  access-pending experience.
- Users with effective permissions receive capability-composed shell/navigation.
- Feature access composition uses resolved capabilities; data-scope filtering
  remains a separate policy layer.

## Enforcement Requirements

- Default is deny unless explicitly allowed.
- Sensitive API endpoints and privileged job paths must enforce explicit
  permission checks.
- Authorization logic should be implemented in dedicated permission
  classes/policies, not inline in view handlers.
- Delegated role/permission assignment must enforce non-delegable permission
  boundaries.
- Direct user permissions are additive exception controls and must not replace
  role-based assignment as the default operating model.

## Security Review Expectations

- Verify deny-by-default behavior on protected endpoints and privileged jobs.
- Verify delegated-assignment guardrails and non-delegable boundaries.
- Verify auth/session control behavior against accepted ADR policy.
- Verify auditability of privileged-access changes and auth/security events.

## Required Test Coverage

- Authorization denial tests for protected workflows.
- Effective-permission resolution tests:
  - multi-role outcomes
  - direct-user permission extension outcomes
  - no-access outcomes
- Auth/session hardening tests:
  - timeout behavior
  - revocation behavior
  - re-authentication and step-up behavior
- Login abuse and MFA tests:
  - success
  - failure
  - recovery paths

## Related

- [`docs/adr/0005-rbac-model-and-permission-enforcement.md`](../adr/0005-rbac-model-and-permission-enforcement.md)
- [`docs/adr/0016-high-assurance-auth-and-session-security-baseline.md`](../adr/0016-high-assurance-auth-and-session-security-baseline.md)
- [`docs/standards/security.md`](./security.md)
- [`docs/standards/testing.md`](./testing.md)
