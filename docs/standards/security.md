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
