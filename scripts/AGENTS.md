# Scripts Guidelines

## Scope
- Applies to `scripts/**`. Follow this file instead of the repo root guidance when they overlap.

## Script Standards
- Follow `docs/standards/scripts.md` and `scripts/README.md`.
- Scripts must be small, single-purpose, safe, and idempotent by default.
- Start shell scripts with `set -euo pipefail`.
- Reuse `scripts/lib/common.sh` for shared helpers instead of duplicating flags, logging, or validation logic.

## Interface and Behavior
- Prefer explicit flags and input validation. Destructive operations should require explicit confirmation flags.
- Avoid implicit side effects and avoid writing output files unless the command is explicitly for export or artifact generation.
- If a script mutates state, prefer a `--dry-run` mode when practical and log what changed.

## Repo Conventions
- Local development and ops flows should stay Docker-first.
- CI scripts should map cleanly to the repo-root `pnpm ci:*` entrypoints.
- If a script requires host-installed dependencies, document that in the closest README or runbook and keep a Docker-based path when possible.
- Keep `scripts/README.md` and `docs/runbooks/local-development.md` aligned with any new developer-facing script such as local seeding or smoke-test helpers.
