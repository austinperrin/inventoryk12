# Data Standards

## Naming

- Use consistent naming for tables and fields.
- For effective date windows, use `starts_on` and `ends_on`.
- Reserve `*_at` for timestamps/events (for example `created_at`, `verified_at`).
- Use Django default `BigAutoField` for internal primary keys.
- Use a separate `uuid` field for stable external/outbound identifiers.

## Common Audit Fields

- Prefer shared abstract model(s) for cross-domain audit attribution fields.
- Baseline common fields for operational entities:
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`
- Keep these fields nullable where workflows are asynchronous or system-driven.
- Lifecycle fields such as `activated_at`, `inactivated_at`, and `inactivated_by`
  should be added only to models that require account-state tracking.

## Change History

- Use `django-simple-history` for model-level change history.
- Exclude sensitive and high-noise fields from history where appropriate
  (for example: `password`, `last_login`, token-like values).
- For sensitive actions, store event metadata without storing secret values.

## Deletion

- Prefer soft deletes for sensitive records unless explicitly required.
