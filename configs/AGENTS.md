# Configuration Guidelines

## Scope
- Applies to `configs/**`. Follow this file instead of the repo root guidance when they overlap.

## Boundaries
- `configs/` is for runtime configuration templates and support files, not committed secrets.
- Current local env templates live under `configs/env/` and are consumed by the bootstrap scripts.
- Security and governance policy documentation belongs in `docs/`, not in configuration templates.

## Conventions
- Keep configuration templates aligned with the actual variables expected by scripts, Docker compose, and service settings.
- Prefer documenting new variables near the bootstrap flow and the consuming service docs when a config surface changes.
- Do not hard-code credentials, real tenant data, or environment-specific secrets in this directory.
