# ADR 0015: Integrations Domain Model

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

The integrations domain owns external system mapping, import/export job metadata,
and synchronization state needed for SIS and partner integrations.

## Decision

- `integrations` owns source-system mapping and sync metadata.
- Integrations orchestrates data movement and reconciliation context but does
  not own core business entities from other domains.
- Unknown external roles/data should default to safe/least-privilege handling
  and require review workflows.

## Model and Field Breakdown

- `IntegrationConnector` (planned)
  - Required: `system_code`, `name`, `is_active`
  - Included: `connection_type`, `base_url`, `auth_method`, `poll_interval_minutes`
- `IntegrationMapping` (planned)
  - Required: `system_code`, `entity_type`, `external_id`, `internal_uuid`
  - Included: `mapping_status`, `last_seen_at`, `metadata`
- `ImportJobRun` / `ExportJobRun` (planned)
  - Required: `system_code`, `job_type`, `status`, `started_at`
  - Included: `completed_at`, `requested_by_user_id`, `result_summary`, `error_count`, `warning_count`
- `SyncCheckpoint` (planned)
  - Required: `system_code`, `entity_type`, `checkpoint_value`
  - Included: `last_synced_at`, `status`, `error_message`

## Expected Constraints (Planned)

- Mapping uniqueness is enforced per source and entity (`system_code`,
  `entity_type`, `external_id`).
- Job run models enforce valid time windows (`completed_at >= started_at`) and
  append-only execution history.
- Checkpoint updates are monotonic per (`system_code`, `entity_type`) unless an
  explicit replay/reset operation is authorized.

## Consequences

- Positive:
  - Isolates integration complexity away from core domain models.
  - Supports repeatable, auditable import/export workflows.
- Tradeoffs:
  - Integration mapping mistakes can propagate across domains.
  - Requires robust monitoring/retry/alerting discipline.

## Alternatives Considered

- Keep integration mappings inside each business domain.
  - Rejected due to duplication and weak operational visibility.
- Build integrations as separate external service from day one.
  - Deferred pending scaling/operational needs.

## Follow-Up

- Define connector configuration security model and secret handling approach.
- Define reconciliation error taxonomy and remediation workflow.
- Define import/export idempotency and replay strategy.

## Review Sign-off Checklist

- [ ] Integration ownership boundaries confirmed
- [ ] Mapping and sync model confirmed
- [ ] Cross-domain reconciliation policy confirmed
- [ ] Operational reliability policy confirmed

## Related ADRs

- Dependencies: `docs/adr/0004-domain-boundaries-and-ownership.md`, `docs/adr/0005-rbac-model-and-permission-enforcement.md`
- Adjacent: `docs/adr/0014-operations-domain-model-v1.md`

## References

- `services/inventory-backend/apps/integrations/`
