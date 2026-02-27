# ADR 0013: Inventory Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The inventory domain is core to the product and owns asset registry, asset
state, assignment/custody lineage, and catalog metadata.

## Decision

- `inventory` owns asset master records and inventory-specific code tables.
- Inventory owns custody/assignment records for assets over time.
- Inventory references identity, organization, and locations for scoped
  assignment context.
- Inventory changes requiring operational workflow transitions are coordinated
  with `operations` domain records.

## Model and Field Breakdown

- `AssetTypeCode` / `AssetStatusCode` / `AssetConditionCode` (planned)
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
- `Asset` (planned)
  - Required: `local_id`, `asset_tag`, `asset_type_code_id`, `status_code_id`
  - Included: `serial_number`, `model`, `manufacturer`, `organization_id`, `facility_id`, `purchased_on`, `warranty_ends_on`, `notes`
- `AssetAssignment` (planned)
  - Required: `asset_id`, `assignee_user_id|organization_id|facility_id`, `starts_at`
  - Included: `ends_at`, `assignment_type`, `reason`, `is_primary`
- `AssetIdentifier` (planned)
  - Required: `asset_id`, `identifier_type`, `identifier_value`
  - Included: `system`, `starts_on`, `ends_on`

## Expected Constraints (Planned)

- Date window checks enforce assignment and identifier validity windows.
- `asset_tag` is unique per tenant scope, and secondary uniqueness constraints
  are defined for identifiers (`asset_id`, `identifier_type`, `identifier_value`).
- Assignment scope requires exactly one assignee target:
  `assignee_user_id` xor `organization_id` xor `facility_id`.

## Consequences

- Positive:
  - Establishes clear ownership of core product data and workflows.
  - Supports auditability of custody and asset state transitions.
- Tradeoffs:
  - Inventory has broad dependencies and high change impact.
  - Requires careful performance planning for high-volume assignment history.

## Alternatives Considered

- Split custody into operations domain from the start.
  - Deferred; custody remains inventory-owned in v1 for coherence.
- Minimal asset-only model with no custody timeline.
  - Rejected due to core accountability requirements.

## Follow-Up

- Define asset identifier and uniqueness policy.
- Define assignment/custody transition state machine.
- Define archival/inactivation policy for retired assets.

## Review Sign-off Checklist

- [ ] Inventory ownership boundaries confirmed
- [ ] Asset and custody model confirmed
- [ ] Cross-domain assignment reference rules confirmed
- [ ] Lifecycle/state transition policy confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0006-identity-domain-model-v1.md`, `docs/adr/0007-organization-domain-model-v1.md`, `docs/adr/0008-locations-domain-model-v1.md`
- Adjacent: `docs/adr/0014-operations-domain-model-v1.md`

## References

- `services/inventory-backend/apps/inventory/`
