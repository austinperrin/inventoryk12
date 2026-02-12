# ADR 0003: Ingestion Architecture (Per-Product First)

## Title
Ingestion Architecture (Per-Product First)

## Status
Accepted (2026-02-10)

## Context
InventoryK12 needs SIS/roster imports and district-controlled validation and
change thresholds. A centralized ingestion service is a future possibility but
adds complexity early.

## Decision
Implement ingestion pipelines within each product backend (starting with
InventoryK12). For MVP, focus on validation handling and user account provisioning.
Design ingestion logic to allow a future centralized ingestion service if needed.

MVP ingestion flow:
- District uploads CSV files to SFTP.
- Admin can manually upload CSV files in the UI.
- Automated import runs on detection or a schedule.
- If scheduled, admins can manually trigger a run on demand.
- Validation errors are captured and reported in the UI.
- Provisioning creates/updates user accounts based on import data.

## MVP Validation and UI Notes

- CSV import types: users, assets, assignments (exact templates to be defined).
- Required fields must be enforced; invalid rows are rejected with error details.
- Validation errors must include row number, field name, and message.
- Import runs should be idempotent for identical files.
- UI should show import status (queued, running, failed, completed) and error summary.

## Consequences
- Faster MVP delivery with fewer services.
- Import thresholds and configuration are deferred until after MVP.
- Future migration to a shared service remains possible.

# Future Enhancements (Post-MVP)

- Import configuration and thresholds per district.
- Notification hooks (success/failure).
- Scheduled imports.
- Multiple simultaneous imports with queueing.
- Provisioning behavior settings (create/update/disable).

## Alternatives Considered
- Shared ingestion service with event/API distribution.
- Shared ingestion service with direct writes to product databases.

## References
- `docs/overview/inventoryk12-blueprint.md`
