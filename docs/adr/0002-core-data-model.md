# ADR 0002: Core Data Model Baseline

## Title
Core Data Model Baseline

## Status
Proposed

## Context
InventoryK12 needs a shared understanding of core entities and required fields
to support MVP workflows and reporting. The initial model will evolve.

## Decision
Establish an initial baseline for core entities and required fields. The model
is a starting point and will evolve as MVP scope is validated.

Baseline entities:
- Asset
  - Asset tag (optional), UUID, serial, manufacturer, model, device type, specs.
  - Purchase date, warranty end, funding source, cost.
  - Status (in service, lost, repair, retired), condition.
  - Current location (org unit), current assignee user, last seen.
- Assignment history
  - Asset, person or org unit, start/end timestamps, notes.
- System audit log (immutable)
  - User, action, target, timestamp, metadata.
- Device history (immutable)
  - Asset, assignee user or org unit, start/end timestamps.
- Discrepancy audit (immutable)
  - Scope (org unit), expected vs found, missing, scan metadata, timestamps.
- Incident
  - Type (damage, loss, theft), reported by, date, status, resolution.
- User profile
  - Role, portal type, contact info.
- Org unit (locations and hierarchy)
  - Name, type, parent org unit (reassignable).

Code tables (per-domain, system + district managed):
- AssetStatus
- AssetCondition
- DeviceType
- IncidentType
- IncidentStatus
- OrgUnitType
- Role (if modeled outside Django Groups, include `system_managed` flag)

Model rules:
- Single active assignment per asset (user or org unit).
- Org units form a parent/child tree that can be reassigned over time.
- Audit and history records are append-only (no edits after creation).
- Serial numbers are unique per manufacturer/vendor, not globally.

Future additions may include depreciation schedules, insurance claims, and
investigation records.

## Consequences
- Provides a starting point for API design and UI flows.
- Changes should be logged as future ADRs.

## Alternatives Considered
- Delay all data modeling until implementation.

## References
- `docs/standards/data.md`
