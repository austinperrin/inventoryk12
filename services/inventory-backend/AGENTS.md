# Backend Guidelines

## Scope
- Applies to `services/inventory-backend/**`. Follow this file instead of the repo root guidance when they overlap.

## Code Style
- Follow `pyproject.toml`: Python 3.14, Black/Ruff/isort, 100-column lines, and Django mypy settings.
- Keep Python code typed, explicit, and small. Match the existing scaffold style in `apps/common/models/base.py` and `apps/common/api/v1/views.py`.
- Prefer service functions over fat model methods. Keep import-time side effects out of modules.

## Architecture
- The backend is intentionally minimal. Shared cross-cutting code belongs in `apps/common`; do not invent new domain apps unless the roadmap or ADRs require the next slice.
- Keep API paths versioned under `/api/v1/<domain>/`; shared scaffold endpoints stay under `/api/v1/common/`.
- Keep configuration in `config/settings/{base,dev,test,prod}.py`, not ad hoc across the codebase.
- Preserve the current scaffold boundary: `apps/common` is for base models, audit helpers, and service-wide utilities, not placeholder domain logic.

## Build and Test
- Default local verification path is repo-root `pnpm dev:checks`.
- Use repo-root wrappers when possible: `pnpm ci:backend`, `pnpm ops:makemigrations`, and `pnpm ops:migrate`.
- Expand tests in `tests/`; the current baseline starts at `tests/test_smoke.py`.

## Security
- Do not reintroduce Django admin as a shortcut; use purpose-built management views and keep privileged actions auditable.
- Preserve HTTPS, secure-cookie, CSRF, and audit-log expectations when touching auth or sensitive workflows.
- Authorization should stay least-privilege and deny-by-default. RBAC definitions and seeded roles belong in `docs/adr/0005-rbac-model-and-permission-enforcement.md`.
