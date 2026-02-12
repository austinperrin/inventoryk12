# InventoryK12

InventoryK12 is a single-product monorepo containing the core InventoryK12
backend/frontend, add-on services/modules, standards, and operational tooling.

## Project Status

- Core repo structure and tooling are scaffolded.
- Backend (Django) and frontend (Vite + React + TS) are in place.
- Compliance and policy docs are placeholders to be filled by the next team.
- Infrastructure is intentionally stubbed until requirements are finalized.

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
   - Python 3.14.3 (only if running backend outside Docker)
2. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env --with-secrets`
3. Configure database (remote or local Postgres):
   - Set `DATABASE_URL` in `.env.backend` to a remote Postgres instance
   - For local Postgres on host, use `host.docker.internal` from Docker
4. Run checks:
   - `pnpm dev:checks`
5. Start services (Docker required):
   - `pnpm dev:up --build --frontend`

## Docs Index

- Review `docs/index.md` for the documentation tree.
