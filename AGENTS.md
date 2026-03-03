# Project Guidelines

## Scope
- This root file applies repo-wide. When editing files under a service, follow the nearest nested `AGENTS.md` first.
- Keep changes small and incremental. Avoid large structural refactors without explicit approval when a targeted change will solve the task.

## Repo Shape
- This is a scaffold-first monorepo. The active services are `services/inventory-backend` and `services/inventory-frontend`; root `package.json` is the main task entrypoint.
- Local development is Docker-first. Compose lives in `infra/docker/docker-compose.dev.yml` and reads root `.env.backend` and `.env.frontend`.
- Treat `docs/roadmap/index.md` as the sequencing source of truth and `docs/adr/0001-tech-stack-and-runtime-baseline.md` as the runtime/platform source of truth before changing stack, deployment, auth, storage, or worker assumptions.

## Shared Tooling
- Required JS toolchain: Node 24.13.0 and `pnpm@9.12.3`.
- Bootstrap env files with `pnpm bootstrap:env`; add `-- --with-secrets` only when local generated secrets are needed.
- Start dev services with `pnpm dev:up` for backend only or `pnpm dev:up -- --frontend` for backend + frontend; add `-- --build` after image or dependency changes.
- Default local verification is `pnpm dev:checks`. Formatting is `pnpm dev:format`.
- CI-equivalent entry points are `pnpm ci:backend`, `pnpm ci:frontend`, `pnpm ci:security`, and `pnpm ci:checks`.
- Use wrapped ops commands instead of ad hoc database flows when possible: `pnpm ops:makemigrations`, `pnpm ops:migrate`, `pnpm ops:backup`, `pnpm ops:restore`, `pnpm ops:reset-schema`.
- Use `pnpm dev:seed-auth-user -- --docker` for the default local browser-login smoke test instead of ad hoc shell commands.
- Local browser URLs should mirror the tenant deployment shape, for example `http://demoisd.localhost:5173/dev/login` and `http://demoisd.localhost:8000/dev/api/v1/common/health/`.

## Shared Conventions
- Shell scripts must stay small, idempotent, and defensive: start with `set -euo pipefail` and reuse `scripts/lib/common.sh` per `scripts/README.md` and `docs/standards/scripts.md`.
- If behavior changes, update the nearest relevant docs in `docs/`, especially `docs/standards/`, roadmap files, or ADRs when the change affects repo-wide assumptions.
- Never commit secrets or real sensitive data. Treat student and tenant data as sensitive by default and redact PII from logs, fixtures, exports, and support tooling.
