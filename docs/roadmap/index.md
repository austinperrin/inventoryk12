# InventoryK12 Roadmap Index

This index is the canonical schedule and progress view from empty repository to
production MVP pilot, plus post-MVP enhancement hooks.

## Team Model

| Team | Responsibility Scope |
| --- | --- |
| Product Management + TPM | Scope, sequencing, commitments, weekly planning/review |
| Architecture | ADR quality, cross-domain decisions, technical guardrails |
| Backend Engineering | Domain models, APIs, migrations, backend tests |
| Frontend Engineering | UI workflows, forms, client validation, frontend tests |
| Data + Integrations | Import/export pipelines, connectors, sync quality |
| Security + Compliance | RBAC, PII controls, audit requirements, evidence |
| DevOps + SRE | CI/CD, deployment, observability, runtime operations |
| QA + Testing | Test planning, regression coverage, release confidence |
| Docs + Standards | Documentation quality, drift-control, standards alignment |

## Schedule

| Milestone | Stage/Phase | Estimate | Planned Start | Planned End | Actual Start | Actual End | Variance | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Milestone 0: Repository Bootstrap](./m0-repository-bootstrap.md) |  | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | In Progress |
|  | [Phase 1: Repo Scaffold and Guardrails](./m0-repository-bootstrap.md#m0-phase-1) | 2-4 days | TBD | TBD | TBD | TBD | TBD | In Progress |
|  | [Phase 2: Standards and Workflow Wiring](./m0-repository-bootstrap.md#m0-phase-2) | 2-3 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Baseline CI and Quality Gate](./m0-repository-bootstrap.md#m0-phase-3) | 2-3 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 1: Platform Baseline](./m1-platform-baseline.md) |  | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Backend/Frontend Skeleton](./m1-platform-baseline.md#m1-phase-1) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Auth and Core Runtime Plumbing](./m1-platform-baseline.md#m1-phase-2) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Local Dev + Ops Baseline](./m1-platform-baseline.md#m1-phase-3) | 3-5 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 2: Domain Foundation](./m2-domain-foundation.md) |  | 3-5 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Identity and Organization](./m2-domain-foundation.md#m2-phase-1) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Locations, Contacts, Academic](./m2-domain-foundation.md#m2-phase-2) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Domain Validation and Migration Freeze](./m2-domain-foundation.md#m2-phase-3) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 3: Access and Environment Controls](./m3-access-and-environment-controls.md) |  | 2-4 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: RBAC Enforcement](./m3-access-and-environment-controls.md#m3-phase-1) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: URL/Topology Routing Baseline](./m3-access-and-environment-controls.md#m3-phase-2) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Non-Prod Refresh Operations](./m3-access-and-environment-controls.md#m3-phase-3) | 3-5 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md) |  | 4-6 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Inventory + Operations Backend Slice](./m4-inventory-mvp-build.md#m4-phase-1) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Frontend Workflow Slice](./m4-inventory-mvp-build.md#m4-phase-2) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: End-to-End QA Gate](./m4-inventory-mvp-build.md#m4-phase-3) | 1 week | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 5: Production Deployment Readiness](./m5-production-deployment-readiness.md) |  | 2-4 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Deployment Pipeline and Infra Baseline](./m5-production-deployment-readiness.md#m5-phase-1) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Security, Backup, Recovery Controls](./m5-production-deployment-readiness.md#m5-phase-2) | 4-6 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Production Dry Run](./m5-production-deployment-readiness.md#m5-phase-3) | 3-5 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 6: MVP Pilot Launch](./m6-mvp-pilot-launch.md) |  | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Pilot Tenant Onboarding](./m6-mvp-pilot-launch.md#m6-phase-1) | 3-5 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Pilot Execution and Support](./m6-mvp-pilot-launch.md#m6-phase-2) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 3: Pilot Exit and MVP Sign-Off](./m6-mvp-pilot-launch.md#m6-phase-3) | 3-4 days | TBD | TBD | TBD | TBD | TBD | Not Started |
| [Milestone 7: Post-MVP Enhancements Hook](./m7-post-mvp-enhancements.md) |  | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 1: Prioritization and ADR Gap Review](./m7-post-mvp-enhancements.md#m7-phase-1) | 2-3 days | TBD | TBD | TBD | TBD | TBD | Not Started |
|  | [Phase 2: Enhancement Backlog and Delivery Plan](./m7-post-mvp-enhancements.md#m7-phase-2) | 2-3 days | TBD | TBD | TBD | TBD | TBD | Not Started |

## Dependency Rules

- Milestones are sequential; only one milestone is active at a time.
- Phases are sequential inside each milestone.
- Work starts on a milestone only when prior milestone is `Completed`.

## Required Controls Per Milestone/Phase

- Pre-Checklist (alignment and drift control)
- Development Checklist (small, PR-sized tasks)
- Review Checklist (quality and sign-off)
- Exit Criteria
- ADR links and ADR gap callouts
