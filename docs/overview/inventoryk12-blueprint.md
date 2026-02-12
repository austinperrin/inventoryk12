# InventoryK12 Blueprint

## Purpose
InventoryK12 is a K-12 asset inventory platform that helps districts track,
assign, audit, and maintain devices and equipment. The product prioritizes
chain-of-custody, auditability, and district-friendly workflows.

## Target Users and Roles
- District admins (policy, configuration, reporting).
- Campus admins and asset managers (daily operations).
- Staff and teachers (assigned device visibility and requests).
- Students (device assignment visibility and check-in/out).
- Parents/guardians (assigned device visibility and policy acknowledgment).

## Portals
- Parent portal, student portal, staff portal.
- Role-based views on a shared underlying UI.
- Future option to split login requirements per portal by district policy.

## Core Workflows (MVP)
- Asset intake and tagging (bulk import + barcode/QR).
- Check-in / check-out for students and staff.
- Inventory audits (scan to reconcile expected vs found).
- Loss/damage reporting with status tracking.
- Notifications for overdue devices and warranty expiration.

## Domain Concepts
- Assets and asset types (devices, peripherals, equipment).
- Assignments and chain-of-custody history.
- Audits as “expected vs found” inventory reconciliations.
- Incidents for damage, loss, or theft.
- Locations (district, campus, building, room).
- Users and roles with least-privilege access.

## Data Model (Starting Point)
This baseline is expected to evolve; changes should be recorded in ADRs.

- Asset
  - Asset tag, UUID, serial, manufacturer, model, device type, specs.
  - Purchase date, warranty end, funding source, cost.
  - Status (in service, lost, repair, retired), condition.
  - Location (campus, building, room), assigned user, last seen.
- Assignment history
  - Asset, person, start/end timestamps, checkout method, notes.
- Audit record
  - Scope (district/campus/building/room/person).
  - Expected count, found count, missing count.
  - Scan metadata and timestamps.
- Incident
  - Type (damage, loss, theft), reported by, date, status, resolution.
- User profile
  - Role, campus, portal type, contact info.

## Integrations
- MVP: CSV via SFTP with manual import trigger in the UI.
- Future: OneRoster, LDAP/Azure Entra for provisioning.
- API import/export for district systems (phase after MVP).
- Remote device management later (Google first, Apple later).

## Reporting and Analytics
- Device utilization.
- Audit accuracy and reconciliation trends.
- Loss/damage rates by campus or device type.

### MVP Reporting (Minimal)

- Asset list with filters (status, condition, device type, org unit, assignee).
- Assignment history per asset and per user.
- Audit discrepancy view (expected vs found, missing by org unit).
- Incident list with filters (type, status, date range, org unit).

## Security and Compliance
- SSO/MFA planned, least privilege enforced.
- PII handled per `docs/standards/security.md`.

## Roadmap Link
- `docs/overview/roadmap.md`
