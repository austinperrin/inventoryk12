# Security Standards

## Secrets

- Never commit secrets to version control.
- Store secrets in environment variables or approved secret managers.
- Rotate secrets when compromise is suspected or after privileged incidents.

## Data Handling

- Assume student data is sensitive by default.
- Redact PII from logs.
- Apply least-data principles in non-prod and support workflows.

## Access Control

- Enforce least privilege in all roles and permissions.
- Default to deny unless explicitly allowed.
- Enforce permission checks on all sensitive API endpoints and privileged jobs.
- Record audit trails for privileged access changes and sensitive actions.
- Enforce login abuse protections on authentication endpoints (throttling/rate
  limiting).
- Enforce session hardening controls for idle timeout and absolute session
  lifetime on session refresh paths.
- Enforce MFA for `system_admin` and support district policy controls for
  global or role-based MFA enforcement with optional user opt-in.
- Enforce client-side timeout UX handling so expired sessions proactively sign
  users out and present clear, scoped sign-in feedback for inactivity versus
  lifetime expiry.
- Treat platform operator authority (`is_staff`/`is_superuser`) as
  infrastructure-level access that is separate from district-managed RBAC
  groups and restricted to InventoryK12 internal support workflows.

## RBAC Source of Truth

- Seeded roles (system-managed):
  - district_admin
  - site_admin
  - system_admin
  - principal
  - teacher
  - counselor
  - aide
  - proctor
  - student
  - parent
  - guardian
  - relative
- RBAC model, delegated administration, seeded roles, and capability matrix are
  defined in `docs/adr/0005-rbac-model-and-permission-enforcement.md`.
