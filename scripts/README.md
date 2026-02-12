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
