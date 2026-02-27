# ADR 0014: Operations Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The operations domain owns operational workflows (audits, incidents, tasks,
workflow actions) that act on core records across inventory and related domains.

## Decision

- `operations` owns workflow and process-tracking records.
- Operations references business entities in other domains but does not own
  those source-of-truth entities.
- Operations maintains status transitions, action logs, and resolution metadata
  for operational processes.

## Model and Field Breakdown

- `AuditRun` (planned)
  - Required: `organization_id|facility_id`, `started_at`, `status`
  - Included: `ended_at`, `scope_definition`, `started_by_user_id`, `notes`
- `AuditDiscrepancy` (planned)
  - Required: `audit_run_id`, `asset_id`, `discrepancy_type`, `status`
  - Included: `expected_value`, `observed_value`, `resolved_at`, `resolved_by_user_id`, `resolution_notes`
- `Incident` (planned)
  - Required: `incident_type`, `status`, `reported_at`
  - Included: `asset_id`, `reported_by_user_id`, `assigned_to_user_id`, `severity`, `description`, `resolved_at`
- `OperationalTask` (planned)
  - Required: `task_type`, `status`, `created_at`
  - Included: `due_at`, `assigned_to_user_id`, `organization_id`, `facility_id`, `metadata`
- `OperationEventLog` (planned)
  - Required: `entity_type`, `entity_id`, `event_type`, `event_at`
  - Included: `actor_user_id`, `payload`

## Expected Constraints (Planned)

- Date/time window checks enforce `ended_at >= started_at` and valid resolution
  timing.
- Scope xor checks enforce single-scope records where required
  (`organization_id` xor `facility_id`).
- Status transitions are constrained by explicit workflow state machines and are
  fully auditable via `OperationEventLog`.

## Consequences

- Positive:
  - Separates workflow process state from source business records.
  - Supports operational reporting and accountability.
- Tradeoffs:
  - Requires robust reference integrity across multiple domains.
  - Workflow complexity can grow quickly without strict state governance.

## Alternatives Considered

- Put audits/incidents directly inside inventory domain.
  - Rejected to preserve separation of process vs source data ownership.
- Create separate domains for each workflow type at v1.
  - Deferred to avoid over-fragmentation.

## Follow-Up

- Define workflow state machine conventions and transition audit policy.
- Define discrepancy taxonomy and resolution requirements.
- Define retention policy for operation logs/events.

## Review Sign-off Checklist

- [ ] Operations ownership boundaries confirmed
- [ ] Workflow entity set confirmed
- [ ] Cross-domain reference policy confirmed
- [ ] State transition governance confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0013-inventory-domain-model-v1.md`
- Adjacent: `docs/adr/0015-integrations-domain-model-v1.md`

## References

- `services/inventory-backend/apps/operations/`
