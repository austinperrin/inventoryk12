# ADR 0007: Organization Domain Model

- **Status**: Accepted
- **Date**: 2026-03-03
- **Owners**: Platform Team

## Context

The organization domain defines district/campus/department structures, hierarchy,
lifecycle, and organizational identifiers used for scoping permissions and
operations.

## Decision

- `organization` owns institutional hierarchy and organization metadata.
- Organization hierarchy is explicit and supports parent/child traversal.
- Organization lifecycle windows are tracked separately from core organization
  identity records.
- Additional external/source identifiers are first-class records.
- The baseline seeded `OrganizationTypeCode` catalog is aligned to OneRoster
  organization types for `district`, `school`, and `department`.

## Model and Field Breakdown

- Baseline field patterns:
  - organization identity and display attributes on `Organization`
  - lifecycle windows (`starts_on`, `ends_on`) in dedicated lifecycle model
  - address links via location/address structures

- `OrganizationTypeCode`
  - Required: `local_id`, `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
  - Seed baseline: `district`, `school`, and `department`
- `Organization`
  - Required: `local_id`, `name`, `organization_type_code_id`
  - Included: `display_name`, `short_name`, `sort_order`, `parent_id`
- `OrganizationLifecycle`
  - Required: `organization_id`, `starts_on`
  - Included: `ends_on`, `note`
- `OrganizationAddress`
  - Required: `organization_id`, `address_id`, `address_type`
  - Included: `is_primary`, `source_system`, `source_record_id`, `starts_on`, `ends_on`
- `OrganizationAdditionalIdentifier`
  - Required: `organization_id`, `system`, `identifier_type`, `identifier_value`
  - Included: `starts_on`, `ends_on`

## Consequences

- Positive:
  - Strong org scoping foundation for RBAC and reporting.
  - Handles structural changes without overwriting history.
- Tradeoffs:
  - Hierarchy integrity constraints must be actively validated.
  - Cross-domain references to organizations must remain consistent during
    org structure changes.

## Alternatives Considered

- Embed lifecycle fields directly on `Organization` only.
  - Rejected in favor of explicit lifecycle records.
- Use generic key/value identifiers instead of typed identifier models.
  - Rejected for weaker integrity and validation.

## Follow-Up

- Swap `OrganizationAddress.address_id` to a real foreign key when the owning
  address model is implemented in the locations/contacts phase.
- Extend organization type taxonomy and governance beyond the baseline
  OneRoster-aligned seed set as needed.
- Define hierarchy change/audit rules for merges and reparent operations.
- Define canonical org scoping policy for role assignments and data queries.

## Review Sign-off Checklist

- [x] Organization hierarchy model confirmed
- [x] Lifecycle model confirmed
- [x] Additional identifier policy confirmed
- [x] Organization scoping rules confirmed

## Related ADRs

- Dependencies: [ADR 0004](./0004-domain-boundaries-and-ownership.md)
- Adjacent: [ADR 0006](./0006-identity-domain-model-v1.md), [ADR 0008](./0008-locations-domain-model-v1.md)

## References

- `services/inventory-backend/apps/organization/`
