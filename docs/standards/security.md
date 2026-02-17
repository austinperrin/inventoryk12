# Security Standards

## Secrets

- Never commit secrets to version control.
- Store secrets in environment variables or secret managers.

## Data Handling

- Assume student data is sensitive by default.
- Redact PII from logs.

## Access Control

- Enforce least privilege in all roles.

## RBAC (Single-District Deployments)

We use Django Groups + Permissions as the primary RBAC mechanism. Each deployed
stack serves a single district, so roles are not tenant-scoped.

### Seeded Roles (System-Managed)

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

These roles are pre-seeded on onboarding and carry default permissions. They
must be marked as system-managed and protected from deletion.

### Custom Roles (District-Managed)

District admins can create additional roles by creating Django Groups in the UI.
Custom roles are district-managed and can be edited or deleted by district admins.

### OneRoster Role Mapping

When ingesting OneRoster users, map OneRoster roles to the seeded roles above.
If a role is unknown, default to the least-privileged role and flag for review.

### Enforcement

- All sensitive endpoints must enforce permission checks in DRF.
- Use group-based permission checks in API views/permissions.
- Role grants should support effective date windows so access can expire by
  assignment without deleting accounts.

### MVP Role Capabilities (Draft)

| Role | Manage Users | Manage Assets | Run Imports | Run Audits | View Reports | Best Suited For |
| --- | --- | --- | --- | --- | --- | --- |
| district_admin | Yes | Yes | Yes | Yes | Yes | District-level IT or asset management leadership |
| site_admin | Limited | Yes | Yes | Yes | Yes | Campus-level asset administrators |
| system_admin | Limited | Yes | Yes | Yes | Yes | IT staff managing system configuration |
| principal | Limited | Yes | Yes | Yes | Yes | Campus principals with oversight |
| teacher | No | Limited | No | No | Limited | Teachers managing assigned classroom devices |
| counselor | No | Limited | No | No | Limited | Counselors with visibility into assignments |
| aide | No | Limited | No | No | Limited | Classroom aides supporting device tracking |
| proctor | No | No | No | No | Limited | Testing coordinators/proctors with read-only access |
| student | No | No | No | No | Limited | Students viewing assigned devices |
| parent | No | No | No | No | Limited | Parents/guardians viewing student devices |
| guardian | No | No | No | No | Limited | Guardians viewing student devices |
| relative | No | No | No | No | Limited | Other authorized family members (if allowed) |

Notes:
- “Limited” means scoped to assigned campus/org unit and read-only where applicable.
- Custom roles can extend or restrict these capabilities.
