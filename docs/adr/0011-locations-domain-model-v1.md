# ADR 0011: Locations Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering

## Context
Locations provides canonical physical address and facility structure for
organization, contacts, and inventory workflows.

## Decision
1. Keep facility hierarchy in `locations.Facility` with optional parent-child
   relationships.
2. Keep facility profile data in `locations.FacilityDetail`.
3. Keep facility lifecycle windows in `locations.FacilityLifecycle`.
4. Keep canonical address models in this domain:
   `locations.Address`, `locations.AddressCatalog`,
   `locations.AddressValidationRun`.
5. Keep geography code tables in this domain:
   `locations.CountryCode` and `locations.StateCode`.
6. Keep facility-to-organization scope link in `locations.OrganizationFacility`.
7. Keep address links on facilities via `locations.FacilityAddress`.
8. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Shared inherited fields for all models in this ADR:
- `id` (internal primary key, `BigAutoField`)
- `uuid` (external identifier, `UUIDField`)
- `created_at`, `updated_at`
- `created_by`, `updated_by`

`CountryCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`StateCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`FacilityTypeCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`Facility`:
- `local_id`, `name`, `display_name`, `short_name`, `sort_order`
- `facility_type_code` (FK)
- `parent` (self FK, nullable)

`FacilityDetail`:
- `facility` (one-to-one FK)
- `floor_plan_url`, `capacity`, `delivery_instructions`, `website_url`, `notes`

`FacilityLifecycle`:
- `facility` (FK)
- `starts_on`, `ends_on`, `note`

`FacilityAddress`:
- `facility` (FK)
- `address_id`
- `address_type`, `is_primary`
- `source_system`, `source_record_id`
- `starts_on`, `ends_on`

`OrganizationFacility`:
- `organization` (FK), `facility` (FK)
- `is_primary`
- `starts_on`, `ends_on`

`FacilityAdditionalIdentifier`:
- `facility` (FK)
- `system`, `identifier_type`, `identifier_value`
- `starts_on`, `ends_on`

`Address`:
- Raw/normalized components:
  `raw_input`, `full_address_text`, `formatted_single_line`, `normalized_hash`
- Parsed components:
  `address_number`, `street_pre_direction`, `street_name`, `street_suffix`,
  `street_post_direction`, `subpremise`, `building`
- Postal components:
  `line_1`, `line_2`, `city`, `county`, `postal_code`, `postal_code_plus4`
- Geography references:
  `state_code` (FK, nullable), `country_code` (FK, nullable)
- Validation metadata:
  `validation_status`, `validation_confidence`, `validation_provider`,
  `validated_at`, `provider_reference`, `validation_payload`

`AddressCatalog`:
- `address` (FK)
- `label`, `catalog_key`, `normalized_hash`
- `is_system_managed`, `is_active`
- `match_priority`, `notes`

`AddressValidationRun`:
- `address` (FK)
- `provider_requested`, `status`
- `started_at`, `completed_at`
- `result_code`, `result_message`, `result_payload`
- `external_cost_estimate`

## Consequences
- Centralizes canonical address ownership and avoids duplication.
- Enables gradual validation-provider integration without schema churn.
- Requires cross-domain care when linking location scope to workflows.

## Alternatives Considered
- Keep address/code tables in `contacts`.
- Flatten facility and detail fields into one table.

## Follow-Up
- Add API contracts for location/address CRUD and validation-run visibility.
- Confirm index/constraint coverage after first workflow query patterns are
  measured.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0005-contact-and-address-model-v1.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `services/inventory-backend/apps/locations/models/location.py`
- `services/inventory-backend/apps/locations/models/address.py`
- `services/inventory-backend/apps/locations/migrations/0001_locations_core.py`
