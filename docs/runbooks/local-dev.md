# Local Development Runbook

## Prerequisites

- Docker
- Docker Compose
- Node 24.13.0 (required for pnpm scripts)
- pnpm 9.12.3
- Postgres endpoint reachable from Docker containers

## Setup

1. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env -- --with-secrets`
   - Optional key rotation: `pnpm bootstrap:secrets -- --force`
2. Set `DATABASE_URL` in `.env.backend`:
   - Use a Postgres endpoint reachable from Docker
   - Example local host DB from Docker: `postgres://user:password@host.docker.internal:5432/dbname`
3. Start services:
   - `pnpm dev:up`
   - `pnpm dev:up -- --frontend`

## Checks (Docker-only)

Use the Docker checks service:

- `pnpm dev:checks`

## Backend DB Workflow (Docker)

When backend models change:

- `pnpm ops:makemigrations -- --docker`
- `pnpm ops:migrate -- --docker`

## Final PR Gate

Run the aggregate CI gate before requesting approval:

- `pnpm ci:checks`

## Notes

- Local and production runtime expectations are containerized (Docker-based).
- `.env.backend` and `.env.frontend` live at repo root.
- Docker compose uses `infra/docker/docker-compose.dev.yml`.
- If Docker commands fail, ensure Docker Desktop is running and your user has access to the Docker socket.
