# Access Control Security Review Runbook

Use this runbook to execute and document access-control and auth/session review
checks for scoped changes.

## Scope

- authorization enforcement behavior
- effective-permission resolution behavior
- auth/session hardening behavior
- security evidence capture for review sign-off

## Prerequisites

- local stack is running and healthy
- required env files are present
- latest migrations are applied
- seeded baseline roles/permissions are available for test personas

## Review Workflow

1. Verify authorization denial behavior.
   - Confirm protected endpoints deny unauthorized requests.
   - Confirm privileged job paths deny unauthorized execution.
2. Verify effective-permission resolution behavior.
   - Validate multi-role union behavior.
   - Validate direct-user permission additive behavior.
   - Validate no-access outcome behavior.
3. Verify delegated-assignment guardrails.
   - Confirm non-delegable permissions cannot be granted by bounded admins.
   - Confirm assignment behavior remains within delegated authority.
4. Verify auth/session hardening behavior.
   - Validate idle timeout and absolute lifetime behavior.
   - Validate revocation and re-authentication/step-up behavior.
5. Verify login abuse and MFA behavior.
   - Validate success/failure/recovery paths.
   - Validate lockout/throttling behavior for repeated failures.
6. Verify auditability.
   - Confirm auth/security events are recorded for reviewable outcomes.
   - Confirm privileged-access change events are recorded.

## Evidence Artifacts

- command/test output for relevant backend and frontend checks
- test case mapping to required coverage categories
- failed and denied request examples with expected response shape
- auth/session behavior validation notes
- audit-event samples for auth/security and privileged-access changes

## Baseline Commands

- `pnpm dev:checks`
- `pnpm ci:backend`
- `pnpm ci:frontend`
- `pnpm ci:security`

Use targeted checks as needed when iterating, then rerun baseline checks before
final sign-off.

## Related

- [`docs/standards/access-control.md`](../standards/access-control.md)
- [`docs/standards/security.md`](../standards/security.md)
- [`docs/standards/testing.md`](../standards/testing.md)
