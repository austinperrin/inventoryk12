# ADR 0004: Domain Boundaries and Ownership

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

This ADR defines domain boundaries, ownership rules, and cross-domain
interaction expectations.

## Decision

- Domain boundaries are aligned to app ownership under
  `services/inventory-backend/apps/`.
- Baseline domain set:
  - `identity`
  - `organization`
  - `locations`
  - `contacts`
  - `academic`
  - `instruction`
  - `enrollment`
  - `inventory`
  - `operations`
  - `integrations`
- `common` is a shared support domain for reusable base/audit concerns only and
  must not become a business-domain catch-all.
- Ownership rules:
  - Each model has exactly one owning domain.
  - `identity` is globally referenceable by other domains when identity linkage
    is required.
  - Cross-domain behavior should use references (FK/UUID) and service/API
    boundaries, not data duplication.
  - Domain-specific invariants are enforced in the owning domain.
- Dependency/order baseline for domain model ADRs:
  - identity -> organization -> locations -> contacts -> academic ->
    instruction -> enrollment -> inventory -> operations -> integrations
- Schema and migrations:
  - Migration files remain domain-local to the owning app.
  - Cross-domain foreign keys are allowed when ownership and lifecycle are clear.

## Model and Field Breakdown

- Planned domain scope is:
  - identity: user/profile/role assignment/auth details
  - organization: district/campus hierarchy and identifiers
  - locations: facility/location/address structures
  - contacts: phone/email/address/relationship records
  - academic: academic time/calendar primitives
  - instruction/enrollment/inventory/operations/integrations: defined through
    follow-up ADRs
- Detailed field-level definitions are owned by each domain ADR
  (`0006` through `0015`).

## Consequences

- Positive:
  - Clear ownership reduces schema drift and unclear responsibility.
  - Supports phased implementation by domain.
  - Keeps domain ADRs focused and incremental.
- Tradeoffs:
  - Cross-domain workflows require careful integration contracts.
  - Team discipline is required to avoid “shortcut” coupling across domains.

## Alternatives Considered

- Single large app/domain with shared model namespace.
  - Rejected due to weak ownership boundaries and long-term maintainability
    risks.
- Over-segmented microservice-per-domain from day one.
  - Deferred to avoid early operational complexity.

## Follow-Up

- Confirm dependency direction per domain ADR and document prohibited reverse
  dependencies where needed.
- Define rules for cross-domain service calls/events as integrations expand.
- Define review guardrails for migration PRs that touch multiple domains.
- Execute implementation incrementally as one domain + migration changeset per
  commit.
- Open questions:
  - Do we require explicit anti-corruption layers for integrations crossing
    multiple domains in v1?

## Review Sign-off Checklist

- [ ] Domain list and ownership confirmed
- [ ] Dependency order confirmed
- [ ] Cross-domain ownership rules confirmed
- [ ] Domain ADR sequencing confirmed

## Related

- `docs/adr/0006-identity-domain-model-v1.md`
- `docs/adr/0007-organization-domain-model-v1.md`
- `docs/adr/0008-locations-domain-model-v1.md`
- `docs/adr/0009-contacts-domain-model-v1.md`
- `docs/adr/0010-academic-domain-model-v1.md`
- `docs/adr/0011-instruction-domain-model-v1.md`
- `docs/adr/0012-enrollment-domain-model-v1.md`
- `docs/adr/0013-inventory-domain-model-v1.md`
- `docs/adr/0014-operations-domain-model-v1.md`
- `docs/adr/0015-integrations-domain-model-v1.md`

## References

- `docs/overview/project.md`
- `services/inventory-backend/apps/`
