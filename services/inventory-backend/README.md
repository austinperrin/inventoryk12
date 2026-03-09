# Backend Service

Django + Django REST Framework API service for the monorepo.

## Goals

- Keep API versioning and environment-path routing consistent.
- Preserve security-first auth/session defaults.
- Add domain behavior in roadmap order with focused, test-covered slices.

## Layout

The backend includes shared platform wiring plus milestone-delivered domain
apps.

```
services/inventory-backend/
├── apps/
│   ├── common/          # cross-cutting utilities and health endpoints
│   ├── identity/        # auth, RBAC, session, and access controls
│   ├── organization/    # district/org baseline models
│   ├── locations/       # location hierarchy baseline models
│   ├── contacts/        # contacts baseline models
│   ├── academic/        # academic baseline models
│   ├── instruction/     # instruction baseline models
│   └── enrollment/      # enrollment baseline models
├── config/              # Django project settings module (env aware)
├── manage.py
└── requirements/        # runtime + dev dependencies
```

- `apps/common`: shared models, audit helpers, and baseline service endpoints.
- `apps/identity`: custom user model, auth APIs, permission governance, MFA/session controls.
- Domain apps (`organization`, `locations`, `contacts`, `academic`, `instruction`, `enrollment`) are present from Milestone 2 domain-foundation delivery.
- `config/settings/`: split settings for `base.py`, `dev.py`, `test.py`, `prod.py`, referencing shared env vars loaded via `configs/`.

## API Conventions

- Shared scaffold endpoints live under `/<env>/api/v1/common/`.
- Authentication baseline endpoints live under `/<env>/api/v1/auth/`.
- The root URL config currently exposes `auth` and `common` route groups and keeps the environment-prefixed entrypoint stable.
- Domain endpoints are added under `/api/v1/<domain>/` as milestone work is implemented.
- Breaking API changes should be introduced through ADR review and version planning.

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

- Complete Milestone 3 phases for URL/topology routing and non-prod refresh operations.
- Progress to Milestone 4 inventory + operations MVP slices per roadmap sequencing.
- Keep test coverage and docs synchronized with each phase branch.

## Local Tooling

- Local backend checks and tests are Docker-only through repo wrappers.
- Use `pnpm dev:checks` for default local verification.
- Use ops/seed scripts with `--docker` for local execution.

## Tooling Baseline

- Python tooling policy lives in `pyproject.toml`:
  - Python 3.14
  - `black`, `ruff`, and `isort` formatting/linting baseline
  - `mypy` with Django settings targeting `config.settings.dev`
- Backend Python dependencies are split under `requirements/`:
  - `requirements/base.txt` for runtime packages
  - `requirements/dev.txt` for lint, typecheck, test, and audit tooling
- Repo-root CI and ops wrappers are the supported entrypoints.
- CI scripts are host-runner oriented for GitHub Actions (not Docker-based) and are invoked through `pnpm ci:*` or `scripts/ci/*`.
- Local development remains Docker-first and should not rely on local Python environments.
- Supported entrypoints:
  - `pnpm ci:backend`
  - `pnpm ci:backend:lint`
  - `pnpm ci:backend:typecheck`
  - `pnpm ci:backend:test`
  - `pnpm ops:makemigrations`
  - `pnpm ops:migrate`
