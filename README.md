# InventoryK12

InventoryK12 is a single-product monorepo containing the core InventoryK12
backend/frontend, add-on services/modules, standards, and operational tooling.

## Project Status

- Core repo structure and tooling are scaffolded.
- Backend (Django) and frontend (Vite + React + TS) are in place.
- Compliance and policy docs are scaffolded and should be expanded as controls are finalized.
- Infrastructure is intentionally minimal until target environments are finalized.

## Structure

- `services/` InventoryK12 core services and add-on services/modules
- `packages/` shared libraries and add-on modules used by InventoryK12
- `configs/` environment and policy configuration
- `docs/` documentation, standards, and compliance
- `infra/` infrastructure (docker, terraform)
- `scripts/` automation hooks

## First-Time Setup

1. Install runtimes (needed to run repo scripts locally):
   - Node 24.13.0
   - pnpm 9.12.3
2. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env -- --with-secrets`
   - Optional key rotation: `pnpm bootstrap:secrets -- --force`
3. Configure database (Docker-reachable Postgres):
   - Set `DATABASE_URL` in `.env.backend` to a Postgres endpoint reachable from containers
   - Example local host DB from Docker: `postgres://user:password@host.docker.internal:5432/dbname`
4. Run checks:
   - `pnpm dev:checks`
5. Start services (Docker required):
   - `pnpm dev:up -- --build --frontend`

## Workflow Expectations

- Local development and operations are Docker-based.
- CI checks (`pnpm ci:*`) are validated in GitHub Actions with CI-managed
  dependencies.

## Docs Index

- Review `docs/index.md` for the documentation tree.
