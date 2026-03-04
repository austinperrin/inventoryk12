# Scripts Guide

This directory contains operational and development scripts for the repository.
Scripts are grouped by intent and should be safe, idempotent, and well-documented.

## Structure

- `bootstrap/` initial setup and environment generation
- `dev/` local developer workflows
- `seed/` baseline application seed data workflows
- `ci/` CI entry points
- `release/` versioning and release steps
- `ops/` operational tasks (migrations, backups, schema reset)
- `security/` audits and security tooling
- `compliance/` evidence checks and exports
- `lib/` shared helpers

## Conventions

- All scripts must start with `set -euo pipefail`.
- Use `scripts/lib/common.sh` for shared helpers.
- Keep scripts small and focused.
- Prefer explicit flags and input validation.
- Avoid writing output files unless explicitly requested.

## Shared Helpers

- `scripts/lib/common.sh`
  - `log_info`, `log_warn`, `log_error`
  - `require_cmd`, `require_file`, `repo_root`

## Local Dev Flow

The canonical startup, smoke-test, and troubleshooting flow is documented in
`docs/runbooks/local-development.md`.

## Bootstrap

- `pnpm bootstrap:env`
  - creates `.env.backend` and `.env.frontend` when missing
  - options:
    - `-- --with-secrets`
- `pnpm bootstrap:secrets`
  - generates or rotates the local backend secret key
  - options:
    - `-- --force`

## Development

- `pnpm dev:up`
  - starts the local development stack
  - options:
    - `-- --frontend`
    - `-- --build`
- `pnpm dev:checks`
  - runs Docker-first backend and frontend checks
  - options:
    - `-- --build`
    - `-- --docker`
- `pnpm dev:format`
  - runs backend and frontend formatters in Docker
- `pnpm dev:reset`
  - stops local dev containers and removes volumes
- `pnpm dev:seed-auth-user`
  - creates or replaces the local auth smoke-test user
  - options:
    - `-- --docker`
    - `-- --email <email>`
    - `-- --password <password>`
    - `-- --first-name <name>`
    - `-- --last-name <name>`
## CI Entry Points

- `pnpm ci:docs`
- `pnpm ci:backend`
- `pnpm ci:frontend`
- `pnpm ci:security`
- `pnpm ci:checks`
- `pnpm ci:backend:lint`
- `pnpm ci:backend:typecheck`
- `pnpm ci:backend:test`
- `pnpm ci:frontend:lint`
- `pnpm ci:frontend:test`

## Operations

- `pnpm ops:makemigrations`
  - options:
    - `-- --docker`
- `pnpm ops:migrate`
  - options:
    - `-- --docker`
- `pnpm ops:reset-schema`
  - options:
    - `-- --database <name>`
    - `-- --force`
    - `-- --yes`
    - `-- --allow-remote`
    - `-- --with-makemigrations`
    - `-- --with-migrate`
    - `-- --docker`
- `pnpm ops:backup -- --output <file>`
- `pnpm ops:restore -- --input <file> --yes`

## Seed Commands

- `pnpm seed:contacts-code-tables`
  - seeds baseline contacts code-table values
  - options:
    - `-- --docker`
    - `-- --dry-run`
  - wrapper script:
    - `scripts/seed/seed-contacts-code-tables.sh`
  - seed definitions live under `services/inventory-backend/apps/contacts/seeds/`

- `pnpm seed:identity-code-tables`
  - seeds baseline identity code-table values
  - options:
    - `-- --docker`
    - `-- --dry-run`
  - wrapper script:
    - `scripts/seed/seed-identity-code-tables.sh`
  - seed definitions live under `services/inventory-backend/apps/identity/seeds/`

- `pnpm seed:organization-code-tables`
  - seeds baseline organization code-table values
  - options:
    - `-- --docker`
    - `-- --dry-run`
  - wrapper script:
    - `scripts/seed/seed-organization-code-tables.sh`
  - seed definitions live under `services/inventory-backend/apps/organization/seeds/`

- `pnpm seed:locations-code-tables`
  - seeds baseline locations code-table values
  - options:
    - `-- --docker`
    - `-- --dry-run`
  - wrapper script:
    - `scripts/seed/seed-locations-code-tables.sh`
  - seed definitions live under `services/inventory-backend/apps/locations/seeds/`

## Security

- `pnpm security:deps-audit`
- `pnpm security:sbom -- --output-dir <dir>`

## Compliance

- `pnpm compliance:checklist`
- `pnpm compliance:export -- --output <file.tar.gz>`

## Release

- `pnpm release:prepare`
  - options:
    - `-- --skip-checks`

## Root Convenience Commands

- `pnpm lint`
- `pnpm format`
- `pnpm check`
- `pnpm commitlint`
