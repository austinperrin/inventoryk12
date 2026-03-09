# Backend Guidelines

## Scope
- Applies to `services/inventory-backend/**`. Follow this file instead of the repo root guidance when they overlap.

## Code Style
- Follow `pyproject.toml`: Python 3.14, Black/Ruff/isort, 100-column lines, and Django mypy settings.
- Keep Python code typed, explicit, and small. Match the existing scaffold style in `apps/common/models/base.py` and `apps/common/api/v1/views.py`.
- Prefer service functions over fat model methods. Keep import-time side effects out of modules.

## Architecture
- The backend currently includes `apps/common`, `apps/identity`, and Milestone-2 domain apps (`organization`, `locations`, `contacts`, `academic`, `instruction`, `enrollment`); add new apps only when roadmap or ADR sequencing requires them.
- Keep API paths versioned and environment-prefixed under `/<env>/api/v1/<domain>/`; shared scaffold endpoints stay under `/<env>/api/v1/common/`.
- Keep configuration in `config/settings/{base,dev,test,prod}.py`, not ad hoc across the codebase.
- Preserve the current scaffold boundaries:
  - `apps/common` is for base models, audit helpers, and service-wide utilities
  - `apps/identity` owns the custom user model and auth runtime endpoints

## Build and Test
- Default local verification path is repo-root `pnpm dev:checks`.
- Use repo-root wrappers when possible: `pnpm ci:backend`, `pnpm ops:makemigrations`, and `pnpm ops:migrate`.
- Local backend ops/seeding/checks should run in Docker (`--docker` where applicable); host Python execution is CI-oriented.
- Expand tests in `tests/`; the current baseline includes `tests/test_smoke.py` and `tests/test_auth_api.py`.

## Security
- Do not reintroduce Django admin as a shortcut; use purpose-built management views and keep privileged actions auditable.
- Preserve HTTPS, secure-cookie, CSRF, cookie-path, and audit-log expectations when touching auth or sensitive workflows.
- Authorization should stay least-privilege and deny-by-default. RBAC definitions and seeded roles belong in `docs/adr/0005-rbac-model-and-permission-enforcement.md`.

## Maintenance
- Keep this `AGENTS.md` updated whenever backend architecture, app boundaries, local workflow, test entrypoints, or security expectations change.
