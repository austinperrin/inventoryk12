# ADR 0017: Integrations Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Data + Integrations, Backend Engineering

## Context
Integrations is scaffolded and will own import/export and source mapping
concerns for external systems and future sync workflows.

## Decision
1. Keep source-system registry and synchronization metadata in `integrations`.
2. Baseline entity set should include:
   `source_system`, `import_job`, `record_map`, `sync_log`.
3. Keep canonical business entities in their owning domains; integrations holds
   mapping and job metadata only.
4. Design mappings around stable external identifiers (`uuid`) and source keys,
   not internal numeric primary keys.
5. Preserve identifier contract on integration records:
   internal `id` for FK/storage use, external `uuid` for API/outbound references.

## Model and Field Breakdown
Current implemented models:
- No concrete Django models are implemented yet in `apps/integrations/models/`.

Planned baseline model set for Stage A review:
- `SourceSystem`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `system_key`, `label`, `system_type`, `is_active`, `config_payload`
- `ImportJob`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `source_system`
  - Proposed domain fields: `job_type`, `status`, `started_at`, `completed_at`,
    `result_summary`, `error_payload`
- `RecordMap`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `source_system`
  - Proposed domain fields: `source_record_id`, `target_domain`, `target_uuid`,
    `map_status`, `last_synced_at`
- `SyncLog`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `source_system`, `import_job`
  - Proposed domain fields: `event_type`, `status`, `message`, `payload`

## Domain Review Note
- Field list above for planned models is provisional until Stage A model review
  and migration design are complete.

## Consequences
- Improves boundary clarity for ingestion and synchronization concerns.
- Reduces coupling between external integrations and internal table IDs.
- Requires robust idempotency and retry semantics in job execution layers.

## Alternatives Considered
- Store source mapping columns directly on every domain table.
- Keep import metadata mixed into inventory workflow tables.

## Follow-Up
- Draft baseline integration models and migration chain.
- Add API/import contract ADR for ingestion error handling and replay behavior.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0003-ingestion-architecture.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `docs/overview/roadmap.md`
- `services/inventory-backend/apps/integrations/models/__init__.py`
