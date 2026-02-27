# ADR 0008: Locations Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The locations domain owns physical place structures and address records used by
organization, inventory assignment context, and operations workflows.

## Decision

- `locations` owns facility hierarchy, facility lifecycle, and address models.
- Facilities are typed and can carry additional identifiers.
- Organization-to-facility mapping is explicit through junction models.
- Address normalization/validation support is managed in locations.

## Model and Field Breakdown

- Baseline field patterns:
  - separate type/code tables for controlled values
  - lifecycle windows for facilities
  - explicit mapping model for organization-facility association

- `CountryCode` / `StateCode` / `FacilityTypeCode`
  - Required: `code`
  - Included: `label`, `description`, `sort_order`, `is_system_managed`, `is_active`
- `Facility`
  - Required: `local_id`, `name`, `facility_type_code_id`
  - Included: `display_name`, `short_name`, `sort_order`, `parent_id`
- `FacilityDetail`
  - Required: `facility_id`
  - Included: `floor_plan_url`, `capacity`, `delivery_instructions`, `website_url`, `notes`
- `FacilityLifecycle`
  - Required: `facility_id`, `starts_on`
  - Included: `ends_on`, `note`
- `FacilityAddress`
  - Required: `facility_id`, `address_id`, `address_type`
  - Included: `is_primary`, `source_system`, `source_record_id`, `starts_on`, `ends_on`
- `OrganizationFacility`
  - Required: `organization_id`, `facility_id`
  - Included: `is_primary`, `starts_on`, `ends_on`
- `FacilityAdditionalIdentifier`
  - Required: `facility_id`, `system`, `identifier_type`, `identifier_value`
  - Included: `starts_on`, `ends_on`
- `Address`
  - Required: `line_1`, `city`
  - Included: normalized address parts, `state_code`, `postal_code`, `country_code`, validation fields, provider payload metadata
- `AddressCatalog`
  - Required: `address_id`, `label`, `catalog_key`
  - Included: `normalized_hash`, `is_system_managed`, `is_active`, `match_priority`, `notes`
- `AddressValidationRun`
  - Required: `address_id`, `provider_requested`, `status`
  - Included: `started_at`, `completed_at`, `result_code`, `result_message`, `result_payload`, `external_cost_estimate`

## Consequences

- Positive:
  - Supports consistent place-based scoping and reporting.
  - Provides reusable address foundation across domains.
- Tradeoffs:
  - Address validation flows add operational complexity.
  - Location hierarchy and org mapping changes require careful migration steps.

## Alternatives Considered

- Keep addresses in each business domain independently.
  - Rejected due to duplication and inconsistent validation.
- Put location data under organization domain only.
  - Rejected to preserve clean facility/address ownership.

## Follow-Up

- Define facility hierarchy constraints and cycle detection policy.
- Define address validation provider strategy and failure handling policy.
- Confirm location-level authorization boundaries for operations and inventory.

## Review Sign-off Checklist

- [ ] Facility model boundaries confirmed
- [ ] Address model boundaries confirmed
- [ ] Organization-facility mapping policy confirmed
- [ ] Location lifecycle policy confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`
- Adjacent: `docs/adr/0007-organization-domain-model-v1.md`, `docs/adr/0013-inventory-domain-model-v1.md`

## References

- `services/inventory-backend/apps/locations/`
