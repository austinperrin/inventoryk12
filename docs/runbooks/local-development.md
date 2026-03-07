# Local Development Runbook

Use this runbook to boot the local stack from a clean checkout and verify the
current backend/frontend development flow.

## Scope

- Docker-first local development
- backend + frontend startup
- migration and auth smoke test
- reset and troubleshooting commands

## Prerequisites

- Docker Desktop is running and reachable from the shell
- Node `24.13.0` or the version currently required by the repo toolchain
- `pnpm@9.12.3` or the version pinned in the root `packageManager`
- a Postgres database reachable from Docker containers

## Local URL Shape

The local environment mirrors the tenant deployment shape:

- frontend origin: `http://demoisd.localhost:5173/dev`
- backend origin: `http://demoisd.localhost:8000/dev`

The environment path is config-driven:

- frontend: `VITE_APP_BASE_PATH` in `.env.frontend`
- backend: `APP_ENV_PATH_PREFIX` in `.env.backend`

## First-Time Bootstrap

1. Create env files:
   - `pnpm bootstrap:env`
   - optional local secrets: `pnpm bootstrap:env -- --with-secrets`
2. Confirm `.env.backend` contains a Docker-reachable `DATABASE_URL`.
3. Confirm `.env.frontend` uses the tenant-style local API base:
   - `VITE_API_BASE_URL=http://demoisd.localhost:8000/dev`
4. Run the default verification path:
   - `pnpm dev:checks -- --build`

## Start the Stack

1. Start backend + frontend:
   - `pnpm dev:up -- --frontend --build`
2. In a second terminal, apply migrations:
   - `pnpm ops:migrate -- --docker`

## Smoke Test

1. Verify backend health:
   - `curl http://demoisd.localhost:8000/dev/api/v1/common/health/`
   - expected response: `{"status":"ok"}`
2. Open the frontend:
   - `http://demoisd.localhost:5173/dev/login`
3. Create a local auth test user if needed:
   - `pnpm dev:seed-auth-user -- --docker`
4. Seed baseline code tables if needed:
   - `pnpm seed:code-tables -- --docker`
   - optional targeted seeding:
     - `pnpm seed:code-tables -- --docker --domain instruction`
     - `pnpm seed:code-tables -- --docker --only identity,organization`
   - domain wrappers remain available (for example, `pnpm seed:academic-code-tables -- --docker`)
5. Sign in with:
   - email: `admin@example.com`
   - password: `ChangeMe123!`
   - seeded name: `Demo Admin`
6. Confirm:
   - `/dev/login` redirects to `/dev`
   - header shows `Logout`
   - backend health link loads
7. Confirm invalid in-app path returns 404:
   - `http://demoisd.localhost:5173/dev/invalid-path-example/`

## Reset

- Stop containers and remove local volumes:
  - `pnpm dev:reset`

Use this when:

- container state is inconsistent
- frontend dependency volume is stale
- Redis state should be cleared

## Troubleshooting

### Docker not reachable

- Symptom:
  - `Docker is not reachable`
- Checks:
  - ensure Docker Desktop is running
  - run `docker info`

### Frontend opens but login never sticks

- Symptom:
  - login succeeds but session remains guest
- Likely cause:
  - frontend and backend hosts do not match for cookie scope
- Fix:
  - use `demoisd.localhost` for both frontend and backend URLs
  - restart after env changes:
    - `pnpm dev:up -- --frontend --build`

### Backend checks fail with missing Python package in Docker

- Symptom:
  - package import error during `pnpm dev:checks`
- Fix:
  - rebuild images:
    - `pnpm dev:checks -- --build`

### Frontend editor reports missing modules

- Symptom:
  - IDE cannot resolve React/Vitest modules
- Cause:
  - dependencies may exist only in Docker volumes
- Fix:
  - run `pnpm install --filter inventory-frontend` on the host if editor
    tooling needs local `node_modules`

### Backend container cannot reach local Postgres

- Symptom:
  - migration or startup database connection errors
- Fix:
  - use a Docker-reachable host in `DATABASE_URL`
  - confirm the chosen hostname resolves from inside containers in your local
    environment
