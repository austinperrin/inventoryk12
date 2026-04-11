# InventoryK12

InventoryK12 is a single-product monorepo containing the core InventoryK12
backend/frontend, add-on services/modules, standards, and operational tooling.

## Project Status

- Milestones 0 through 2 are complete: repo bootstrap, platform baseline, and
  domain foundation are in place.
- Milestone 3 is active: backend auth/session hardening, routing baseline, and
  frontend UI baseline are implemented; admin/system management UX and non-prod
  seed/smoke support are still in progress.
- Milestone 4 inventory MVP workflows have not started yet.
- Infrastructure remains intentionally minimal until target deployment
  environments are finalized.

## Structure

- `services/` InventoryK12 core services and add-on services/modules
- `packages/` shared libraries and add-on modules used by InventoryK12
- `configs/` runtime/environment configuration templates
- `docs/` documentation, standards, and compliance
- `infra/` infrastructure (docker, terraform)
- `scripts/` automation hooks

## First-Time Setup

1. Install runtimes (needed to run repo scripts locally):
   - Node 24.13.0 or the version currently required by the repo toolchain
   - `pnpm@9.12.3` or the version pinned in `packageManager`
2. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env -- --with-secrets`
   - Optional key rotation: `pnpm bootstrap:secrets -- --force`
3. Configure database (Docker-reachable Postgres):
   - Set `DATABASE_URL` in `.env.backend` to a Postgres endpoint reachable from containers
   - Example local host DB from Docker: `postgres://user:password@host.docker.internal:5432/dbname`
4. Run checks:
   - `pnpm dev:checks`
   - Rebuild Docker images first if dependencies changed: `pnpm dev:checks -- --build`
5. Start services (Docker required):
   - `pnpm dev:up -- --build --frontend`
6. Apply backend migrations:
   - `pnpm ops:migrate -- --docker`
7. Use the local tenant URL shape:
   - frontend: `http://demoisd.localhost:5173/dev/login`
   - backend: `http://demoisd.localhost:8000/dev/api/v1/common/health/`

## Workflow Expectations

- Local development and operations are Docker-based.
- Local checks/tests should run via Docker-backed wrappers (`pnpm dev:checks`, `pnpm dev:format`) and Docker ops flags (`--docker`) where supported.
- Local backend workflows should not depend on host Python virtual environments.
- CI checks (`pnpm ci:*`) are validated in GitHub Actions with CI-managed
  host-runner dependencies.
- The canonical startup/reset/troubleshooting flow is documented in
  [docs/runbooks/local-development.md](./docs/runbooks/local-development.md).

## Docs Index

- Review [`docs/index.md`](./docs/index.md) for the documentation tree.
