# URL Topology Routing Runbook

Use this runbook to set up and verify tenant/environment routing behavior
aligned with ADR 0002.

## Scope

- tenant host + environment-path routing baseline
- environment target configuration model
- operational checks for configured and unconfigured environment paths

## Inputs

- ADR baseline: `docs/adr/0002-url-and-domain-topology.md`
- routing target template:
  `configs/routing/tenant-environment-routing.example.yaml`
- backend env path prefix:
  `APP_ENV_PATH_PREFIX` in `.env.backend`
- frontend base path:
  `VITE_APP_BASE_PATH` in `.env.frontend`

## Configuration Workflow

1. Copy the routing target template and create a tenant-specific config in your
   deployment tooling context.
2. Ensure each enabled environment includes:
   - `path_prefix`
   - `frontend_origin`
   - `backend_origin`
   - `default_deny_unknown_paths: true`
3. Keep allowlisted environment keys aligned with ADR 0002 intent
   (`prod`, optional non-prod, internal `dev`).

## Local Baseline Validation

Run these checks with Docker services up:

1. Start stack:
   - `pnpm dev:up -- --frontend --build`
2. Ensure backend uses expected env prefix:
   - `.env.backend` has `APP_ENV_PATH_PREFIX=/dev`
3. Ensure frontend path matches:
   - `.env.frontend` has `VITE_APP_BASE_PATH=/dev`
4. Validate configured path health:
   - `curl http://demoisd.localhost:8000/dev/api/v1/common/health/`
   - expected: `200` with `{"status":"ok"}`
5. Validate deny-by-default for an unconfigured environment path:
   - `curl -i http://demoisd.localhost:8000/prod/api/v1/common/health/`
   - expected: `404` when local stack is configured only for `/dev`

## Operational Checks

- Confirm app and API stay under one browser-visible tenant origin per
  environment path.
- Confirm unknown/unconfigured environment paths are denied.
- Confirm environment-path assumptions in frontend/backend env files remain
  consistent after changes.
- Re-run default local checks after routing-related changes:
  - `pnpm dev:checks -- --build`

## Related

- [`docs/adr/0002-url-and-domain-topology.md`](../adr/0002-url-and-domain-topology.md)
- [`infra/docker/README.md`](../../infra/docker/README.md)
- [`docs/runbooks/local-development.md`](./local-development.md)
