# Backend Service

Django + Django REST Framework API scaffold for the monorepo. This document
captures the backend baseline before domain implementation is rebuilt.

## Goals

- Establish a clean backend scaffold for roadmap-driven implementation.
- Keep API versioning consistent from the start.
- Preserve security-first defaults without coupling the scaffold to unfinished domains.

## Layout

The backend currently keeps only shared scaffold components in place. Domain
apps will be reintroduced milestone by milestone as roadmap work is completed.

```
services/inventory-backend/
├── apps/
│   ├── common/          # cross-cutting utilities and health endpoints
├── config/             # Django project settings module (env aware)
├── manage.py
└── docker/             # service-specific Docker assets if needed
```

- `apps/common`: shared models, audit helpers, and baseline service endpoints.
- `apps/common` is registered explicitly via `apps.common.apps.CommonConfig` in `config/settings/base.py`.
- `config/settings/`: split settings for `base.py`, `dev.py`, `test.py`, `prod.py`, referencing shared env vars loaded via `configs/`.
- `docker/`: overrides or extra compose snippets specific to the backend service.

## API Conventions

- Shared scaffold endpoints live under `/<env>/api/v1/common/`.
- Authentication baseline endpoints live under `/<env>/api/v1/auth/`.
- The root URL config currently exposes only the scaffold common endpoints so later domain routes can be added incrementally without reshaping the service entrypoint.
- Domain endpoints are added under `/api/v1/<domain>/` as milestone work is implemented.
- Breaking API changes should be introduced through ADR review and version planning.
- Auth-specific runtime wiring is intentionally deferred to the roadmap platform
  baseline milestone and ADR 0001.

## Security Expectations

- Remove Django admin site; replace with purpose-built management views in domain apps.
- Require HTTPS and secure cookies in prod; CSRF protection for session-based flows.
- Enforce OWASP best practices: rate limiting, input validation, secure headers, audit logging.
- Secrets loaded from environment or secret manager; never hard-coded.

## Deployment Routing Baseline

- Backend services may run on a different server than the frontend, but the browser should still use one public tenant origin.
- For a tenant such as `demoisd`, the public app and API should resolve under the same host, for example `https://demoisd.inventoryk12.com/prod`.
- Edge or gateway routing should forward app traffic to the frontend server and API traffic to the backend server while keeping auth cookies scoped to the public tenant host instead of an internal backend hostname.
- Local development can mirror that structure with hosts such as
  `demoisd.localhost` plus an environment path like `/dev`.

## Next Steps

- Reintroduce backend domain apps in roadmap order.
- Add auth runtime plumbing during the platform baseline milestone and expand
  RBAC behavior during the access-control milestone.
- Expand test coverage as service capabilities are added.

## Local Tooling

- Run backend checks through Docker: `pnpm dev:checks`.

## Tooling Baseline

- Python tooling policy lives in `pyproject.toml`:
  - Python 3.14
  - `black`, `ruff`, and `isort` formatting/linting baseline
  - `mypy` with Django settings targeting `config.settings.dev`
- Backend Python dependencies are split under `requirements/`:
  - `requirements/base.txt` for runtime packages
  - `requirements/dev.txt` for lint, typecheck, test, and audit tooling
- Repo-root CI and ops wrappers are the supported entrypoints:
  - `pnpm ci:backend`
  - `pnpm ci:backend:lint`
  - `pnpm ci:backend:typecheck`
  - `pnpm ci:backend:test`
  - `pnpm ops:makemigrations`
  - `pnpm ops:migrate`
