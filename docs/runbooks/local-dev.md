# Local Development Runbook

## Prerequisites

- Docker
- Docker Compose
- Node 24.13.0 (required for pnpm scripts)
- pnpm 9.12.3
- Postgres (remote or local instance)

## Setup

1. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env --with-secrets`
2. Set `DATABASE_URL` in `.env.backend`:
   - Remote Postgres for dev/prod-like parity
   - Local Postgres example: `postgres://user:password@host.docker.internal:5432/dbname`
3. Start services:
   - `pnpm dev:up`
   - `pnpm dev:up -- --frontend`

## Checks (Docker-only)

Use the Docker checks service:

- `pnpm dev:checks`

## Notes

- `.env.backend` and `.env.frontend` live at repo root.
- Docker compose uses `infra/docker/docker-compose.dev.yml`.
- If Docker commands fail, ensure Docker Desktop is running and your user has access to the Docker socket.
