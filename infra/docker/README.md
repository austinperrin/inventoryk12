# Docker Development

Local development is orchestrated with Docker Compose.

## Commands

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
