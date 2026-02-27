# ADR 0002: URL and Domain Topology

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

This ADR defines public URL structure, domain boundaries, and environment
segmentation across marketing and product surfaces.

## Decision

- Public marketing/website entrypoint:
  - `inventoryk12.com` (and optional `www.inventoryk12.com`)
- Product tenancy URL baseline:
  - tenant hostnames under `inventoryk12.com` (for example:
    `demoisd.inventoryk12.com`)
- Environment selection baseline:
  - Environment is path-based (`/prod`, `/sandbox`, `/training`, etc).
  - Example product login path:
    `https://demoisd.inventoryk12.com/prod/login/`
- Edge routing baseline:
  - Cloudflare Workers perform path-based environment routing.
  - Cloudflare-managed configuration maps tenant+environment path to
    environment-specific origins.
- Origin/service routing baseline:
  - Each environment stack can use Nginx (or equivalent gateway) to route app,
    API, static/media, and service paths within that environment.
- Environment isolation baseline:
  - Each environment maps to dedicated backend/frontend/service deployments.
  - Non-prod and prod do not share runtime resources by default.
- Environment availability baseline:
  - Some tenants may have only prod.
  - Additional environment paths exist only when explicitly configured.
  - Unknown/unconfigured environment paths return deny-by-default responses.
- Environment intent baseline:
  - `prod` is customer-facing production.
  - `sandbox` and `training` are optional customer-facing non-prod
    environments.
  - `dev` is internal support/testing and not customer-facing by default.
- Environment naming baseline:
  - Environment path keys use a standardized allowlist managed by the
    InventoryK12 team.

## Model and Field Breakdown

Not applicable.

## Consequences

- Positive:
  - Preserves your preferred single-label tenant subdomain model.
  - Supports dynamic optional environments per tenant without DNS changes per
    environment.
  - Centralizes routing logic at the edge.
- Tradeoffs:
  - Path-based environment segmentation requires careful auth/cookie and route
    controls.
  - Worker routing configuration becomes a critical operational dependency.

## Alternatives Considered

- Environment-by-subdomain (for example `demoisd-sandbox.inventoryk12.com`).
  - Not selected for baseline due to preference for path-based environment
    navigation.
- Environment-by-separate root domains.
  - Not selected for baseline due to higher domain/certificate management
    complexity.
- Edge routing only with origin Nginx and no Cloudflare Workers.
  - Not selected for baseline due to dynamic tenant environment mapping needs.

## Follow-Up

- Define Worker configuration source and change management workflow.
- Define environment path naming policy and reserved path words.
- Define edge and origin guardrails:
  - deny-by-default for unknown environment paths
  - non-prod indexing controls
  - explicit path-based auth/session isolation rules
- Define DNS/TLS policy in Cloudflare for wildcard and tenant onboarding.
- Define non-prod access control defaults (IP allow list, SSO gate, basic auth)
  by environment class.
- Define onboarding workflow for enabling optional non-prod environments per
  tenant.
- Non-prod data refresh/sanitization policy is addressed in
  `docs/adr/0003-non-prod-data-refresh-and-sanitization-policy.md`.

## Review Sign-off Checklist

- [ ] URL topology baseline confirmed
- [ ] Edge routing model confirmed
- [ ] Environment path policy confirmed
- [ ] Security guardrails confirmed

## Related

- `docs/adr/0001-tech-stack-and-runtime-baseline.md`
- `docs/adr/0003-non-prod-data-refresh-and-sanitization-policy.md`
- `docs/adr/0005-rbac-model-and-permission-enforcement.md`

## References

- `docs/overview/project.md`
