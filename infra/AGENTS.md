# Infrastructure Guidelines

## Scope
- Applies to `infra/**`. Follow this file instead of the repo root guidance when they overlap.

## Current State
- Infrastructure in this repo is intentionally minimal. `infra/docker/` contains the active local development path; `infra/terraform/` is still a stub.
- Do not over-specify production infrastructure that the repo has not implemented yet.

## Docker
- Keep local development changes aligned with `infra/docker/docker-compose.dev.yml` and `infra/docker/README.md`.
- Preserve the Docker-first workflow expected by the repo-root commands such as `pnpm dev:up` and `pnpm dev:checks`.
- Compose changes should continue to rely on root `.env.backend` and `.env.frontend` rather than ad hoc service-local env conventions.

## Terraform
- Treat `infra/terraform/` as reserved structure until provider, state backend, and environment strategy are finalized.
- Do not add environment-specific Terraform assumptions that conflict with ADRs or undocumented deployment decisions.

## Architecture Boundaries
- Before changing deployment topology, tenant/environment isolation, storage, or worker infrastructure assumptions, check `docs/adr/0001-tech-stack-and-runtime-baseline.md` and related ADRs.
