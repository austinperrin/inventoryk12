# ADR 0001: Tech Stack and Runtime Baseline

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

InventoryK12 is being built with low initial cost constraints, GitHub-centric
workflows, and a target deployment model of self-hosted, on-prem-style
infrastructure managed by the InventoryK12 team.

The platform must support:
- Django + DRF backend
- React + Vite + TypeScript frontend
- PostgreSQL data storage
- multi-service/containerized deployments
- future add-ons/microservices
- tenant and environment isolation

## Decision

- Monorepo remains the source of truth for backend, frontend, and service code.
- Core application stack:
  - Backend: Python, Django, Django REST Framework
  - Frontend: React, Vite, TypeScript
  - Database: PostgreSQL (external to app containers)
- Runtime and packaging:
  - Services are containerized with Docker.
  - Local developer and operations flows are Docker-first.
- Asynchronous/background processing:
  - Use worker services for long-running jobs (imports/exports/scheduled tasks).
  - Celery + Redis is the baseline queue/worker model for v1.
  - Background jobs should be implemented behind an internal job abstraction so
    queue backend can be replaced later if needed.
- Deployment model baseline:
  - Isolation boundary is tenant + environment.
  - Baseline hosting model is InventoryK12-managed, in-house, on-prem-style
    deployments.
  - Each tenant environment gets a dedicated application stack deployment.
  - Small deployments may run multiple containers on a single server.
  - Larger deployments may split services across multiple servers.
- Data isolation baseline:
  - Prefer one PostgreSQL database per environment over shared-schema tenancy.
- Storage baseline:
  - Support document/photo uploads and import files.
  - Local disk-backed storage is the baseline for v1.
  - SFTP is supported as an import channel, not as the primary storage model.
  - Storage implementation should preserve a clean path to object storage
    adoption later (for example S3-compatible backends).
- URL and domain topology is intentionally defined separately in
  `docs/adr/0002-url-and-domain-topology.md`.

## Model and Field Breakdown

Not applicable.

## Consequences

- Positive:
  - Uses mature, common enterprise technologies.
  - Keeps initial hosting and operations flexible for low-cost starts.
  - Supports gradual scale-up without immediate platform re-architecture.
- Tradeoffs:
  - Per-tenant/per-environment isolation increases deployment and operations
    overhead.
  - Worker/queue infrastructure adds system complexity but is required for
    reliable large jobs.

## Alternatives Considered

- Shared multi-tenant database/schema model by default.
  - Rejected for baseline due to higher data isolation risk and complexity.
- Single-process app stack with no worker queue.
  - Rejected for baseline due to expected long-running import/export workloads.
- Immediate orchestration-first platform (for example Kubernetes).
  - Deferred to avoid early operational cost/complexity.

## Follow-Up

- Finalize runtime version policy (Python/Node/pnpm support window).
- Define deployment profiles:
  - single-server profile
  - split-service profile
- Define storage implementation detail:
  - local filesystem vs object storage baseline
- Define worker reliability baseline:
  - retries, dead-letter strategy, timeouts, concurrency controls
- Define customer-hosted/on-prem-by-tenant support policy for post-v1 phases.
- Define object storage migration trigger thresholds (data volume/performance).

## Review Sign-off Checklist

- [ ] Platform baseline confirmed
- [ ] Deployment profile policy confirmed
- [ ] Queue/worker baseline confirmed
- [ ] Data isolation baseline confirmed

## Related

- `docs/overview/project.md`
- `docs/adr/0002-url-and-domain-topology.md`

## References

- `docs/standards/coding-standards.md`
- `docs/standards/scripts.md`
- `docs/standards/testing.md`
