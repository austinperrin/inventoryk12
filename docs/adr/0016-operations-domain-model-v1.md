# ADR 0016: Operations Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
Operations will own discrepancy, incident, and activity-log workflows needed
for auditability and compliance but is currently scaffolded.

## Decision
1. Keep operational workflow and audit entities in `operations`.
2. Baseline entity set should include:
   `incident`, `workflow`, and `activity_log`.
3. Keep inventory domain focused on asset/custody records; operations references
   inventory events instead of duplicating inventory state.
4. Require PII-minimized activity metadata and stable event typing.
5. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Current implemented models:
- No concrete Django models are implemented yet in `apps/operations/models/`.

Planned baseline model set for Stage A review:
- `Incident`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `asset`, `reporter_user`, `organization_scope`, `facility_scope`
  - Proposed domain fields: `incident_type`, `severity_code`, `status_code`, `summary`, `details`
  - Proposed lifecycle fields: `reported_at`, `resolved_at`
- `Workflow`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `workflow_type`, `state_code`, `owner_user`, `due_at`
  - Proposed linkage fields: `target_domain`, `target_uuid`
- `ActivityLog`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `event_type`, `event_code`, `message`, `metadata`
  - Proposed linkage fields: `target_domain`, `target_uuid`, `actor_user`

## Domain Review Note
- Field list above for planned models is provisional until Stage A model review
  and migration design are complete.

## Consequences
- Establishes clear ownership for audit and incident lifecycle data.
- Supports security/compliance evidence collection expectations.
- Requires strict event schema discipline to avoid log noise.

## Alternatives Considered
- Keep incident/audit records inside `inventory`.
- Keep all operational events in generic untyped JSON blobs.

## Follow-Up
- Draft operations baseline models and migration chain.
- Define event taxonomy and retention controls in follow-up ADR.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`
- `docs/standards/security.md`

## References
- `docs/overview/roadmap.md`
- `services/inventory-backend/apps/operations/models/__init__.py`
