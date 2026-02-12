# Backend Service

Django + Django REST Framework API that powers the mono-repo. This document captures structural conventions and early scaffolding as the backend evolves.

## Goals

- Single-tenant deployments with per-tenant Postgres database.
- Modular domain apps living under `services/inventory-backend/apps/`.
- Consistent API versioning (`/api/v1/<domain>/...`).
- Security-first defaults (JWT auth, RBAC, no Django admin UI).

## Layout

The domain app structure below reflects current scaffolding and planned
domain growth.

```
services/inventory-backend/
├── apps/
│   ├── common/          # cross-cutting utilities (RBAC base classes, audit helpers)
│   ├── identity/        # tenant identity/IAM domain (users, profiles, SSO connectors)
│   └── ...
├── config/             # Django project settings module (env aware)
├── manage.py
└── docker/             # service-specific Docker assets if needed
```

- `apps/<domain>`: each domain is a Django app with its own `api/v1/<domain>/` namespace (routers, serializers, views).
- `config/settings/`: split settings for `base.py`, `dev.py`, `test.py`, `prod.py`, referencing shared env vars loaded via `configs/`.
- `docker/`: overrides or extra compose snippets specific to the backend service.

## API Conventions

- REST endpoints under `/api/v1/<domain>/` by default; bump versions via ADR when breaking changes occur.
- JWT-based auth with pluggable identity providers per tenant (default Django auth + optional SSO integrations) (planned).
- RBAC enforced in DRF permissions; admin-only features exposed via same endpoints but gated by permissions.

## Security Expectations

- Remove Django admin site; replace with purpose-built management views in domain apps.
- Require HTTPS and secure cookies in prod; CSRF protection for session-based flows.
- Enforce OWASP best practices: rate limiting, input validation, secure headers, audit logging.
- Secrets loaded from environment or secret manager; never hard-coded.

## Next Steps

- Expand identity models as IAM scope grows (providers, external identities).
- Add auth endpoints and RBAC enforcement as the roadmap advances.
- Integrate testing/linting workflow (pytest, mypy, bandit) aligned with CI/CD.

## Local Tooling

- Run type checks with `mypy services/inventory-backend`.
