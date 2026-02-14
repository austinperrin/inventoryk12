# Scripts Guide

This directory contains operational and development scripts for the repository.
Scripts are grouped by intent and should be safe, idempotent, and well-documented.

## Structure

- `bootstrap/` initial setup and environment generation
- `dev/` local developer workflows
- `ci/` CI entry points
- `release/` versioning and release steps
- `ops/` operational tasks (migrations, backups)
- `security/` audits and security tooling
- `compliance/` evidence checks and exports
- `lib/` shared helpers

## Conventions

- All scripts must start with `set -euo pipefail`.
- Use `scripts/lib/common.sh` for shared helpers.
- Keep scripts small and focused.
- Prefer explicit flags and input validation.
- Avoid writing output files unless explicitly requested.

## Dev reset

Run `pnpm dev:reset` to stop dev containers and remove Docker volumes.

## Ops and release commands

- CI:
  - `pnpm ci:backend`
  - `pnpm ci:frontend`
  - `pnpm ci:security`
  - `pnpm ci:checks`
- Migrations:
  - `pnpm ops:makemigrations`
  - `pnpm ops:makemigrations -- --docker`
  - `pnpm ops:migrate`
  - `pnpm ops:migrate -- --docker`
- Backup and restore:
  - `pnpm ops:backup -- --output backups/dev.sql`
  - `pnpm ops:restore -- --input backups/dev.sql --yes`
- Security:
  - `pnpm security:deps-audit`
  - `pnpm security:sbom -- --output-dir artifacts/sbom`
- Compliance:
  - `pnpm compliance:checklist`
  - `pnpm compliance:export -- --output artifacts/compliance-evidence.tar.gz`
- Release:
  - `pnpm release:prepare`
