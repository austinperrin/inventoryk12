# Docker Development

Local development is orchestrated with Docker Compose.

## Commands

- Default checks:
  - `pnpm dev:checks`
- Rebuild images, then run checks:
  - `pnpm dev:checks -- --build`
- Backend only:
  - `pnpm dev:up`
- Backend + frontend:
  - `pnpm dev:up -- --frontend`
- Rebuild images:
  - `pnpm dev:up -- --build`

## Notes

- Uses `.env.backend` and `.env.frontend` from the repo root.
- Requires a Postgres database reachable from the backend container.
- For local Postgres on the host, use `host.docker.internal` in `DATABASE_URL`.
- Frontend is behind the `frontend` compose profile.
- Frontend containers use the root `pnpm-lock.yaml` for installs.
- Frontend uses a named PNPM store volume to avoid host filesystem quirks.
- Local browser URLs should mirror the tenant shape:
  - `http://demoisd.localhost:5173/dev/login`
  - `http://demoisd.localhost:8000/dev/api/v1/common/health/`
- Apply backend migrations after startup:
  - `pnpm ops:migrate -- --docker`
- Seed a local auth test user when needed:
  - `pnpm dev:seed-auth-user -- --docker`
- Reset local state with:
  - `pnpm dev:reset`
- See the full operator flow in
  [docs/runbooks/local-development.md](../../docs/runbooks/local-development.md).
