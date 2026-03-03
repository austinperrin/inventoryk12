# Milestone 2: Domain Foundation

- Status: In Progress
- Estimate: 3-5 weeks
- Dependency: [Milestone 1: Platform Baseline](./m1-platform-baseline.md) `Completed`
- Related ADRs: [ADR 0004](../adr/0004-domain-boundaries-and-ownership.md), [ADR 0006](../adr/0006-identity-domain-model-v1.md), [ADR 0007](../adr/0007-organization-domain-model-v1.md), [ADR 0008](../adr/0008-locations-domain-model-v1.md), [ADR 0009](../adr/0009-contacts-domain-model-v1.md), [ADR 0010](../adr/0010-academic-domain-model-v1.md)

## Owners

- Milestone Owner: Architecture
- Technical Owner: Backend Engineering
- Execution Teams: Backend Engineering, QA + Testing, Docs + Standards

## Goal

Implement and validate foundation domains with clean migration history and
review gates.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [x] Domain order is dependency-aligned.
- [x] Each domain task is PR-sized and branch-planned.
- [x] ADR links for each domain are explicit and current.
- [x] Migration review and rollback approach is documented.
- [x] Roadmap status and owners are current.

## Pre-Checklist Notes

### Domain Order

- Implementation order follows [ADR 0004](../adr/0004-domain-boundaries-and-ownership.md):
  `identity -> organization -> locations -> contacts -> academic`.
- Phase 1 covers `identity` then `organization`.
- Phase 2 covers `locations`, `contacts`, then `academic`.
- Phase 3 validates the combined migration graph and freezes domain shape for
  later milestones.

### Branch and PR Plan

- Milestone branch: `chore/m2-integration`
- Phase 1 branches: `feat/m2-p1-identity-domain`,
  `feat/m2-p1-organization-domain`
- Phase 2 branches: `feat/m2-p2-locations-domain`,
  `feat/m2-p2-contacts-domain`, `feat/m2-p2-academic-domain`
- Phase 3 branch: `chore/m2-p3-domain-freeze-validation`
- All milestone 2 PRs target `chore/m2-integration` until milestone closeout.

### ADR Coverage

- Domain boundaries and dependency order: [ADR 0004](../adr/0004-domain-boundaries-and-ownership.md)
- Identity domain scope: [ADR 0006](../adr/0006-identity-domain-model-v1.md)
- Organization domain scope: [ADR 0007](../adr/0007-organization-domain-model-v1.md)
- Locations domain scope: [ADR 0008](../adr/0008-locations-domain-model-v1.md)
- Contacts domain scope: [ADR 0009](../adr/0009-contacts-domain-model-v1.md)
- Academic domain scope: [ADR 0010](../adr/0010-academic-domain-model-v1.md)

### Migration Review and Rollback Approach

- Keep migrations domain-local under the owning app named in [ADR 0004](../adr/0004-domain-boundaries-and-ownership.md).
- Land one domain changeset per phase branch so migration diffs stay reviewable
  and reversible.
- Use repo wrappers for schema work: `pnpm ops:makemigrations`,
  `pnpm ops:migrate`, and `pnpm ops:reset-schema` when validating graph/reset
  behavior.
- Take a database backup with `pnpm ops:backup` before applying milestone-level
  migration sequences that need rollback coverage.
- Use `pnpm ops:restore` for backup-based rollback when migration reversal is
  insufficient or unsafe.
- Reserve final migration graph validation and reset-path confirmation for
  `chore/m2-p3-domain-freeze-validation` before milestone closeout.

## Execution Model

- Milestone pre-checklist updates should be completed on the milestone branch
  `chore/m2-integration`.
- Each phase branch should be created from `chore/m2-integration`.
- Each phase should be completed on its recommended phase branch.
- Phase-specific checklist and status updates should be committed in that same
  phase branch instead of being deferred.
- Each phase branch should merge back into `chore/m2-integration` after that
  phase is complete.
- The milestone branch `chore/m2-integration` is reserved for milestone-level
  reconciliation, milestone review checklist updates, and the final PR to `main`.

<a id="m2-phase-1"></a>
## Phase 1: Identity and Organization

### Phase Goal
Implement identity and organization domains in a dependency-safe, migration-stable sequence.

### Development Checklist

#### Backend Engineering
- [ ] Implement identity updates from ADR 0006.
- [ ] Implement organization updates from ADR 0007.
- [ ] Build migration chain.

#### QA + Testing
- [ ] Add constraint and lifecycle test coverage.

#### Docs + Standards
- [ ] Update docs for finalized model/migration expectations.

### Branch and PR Plan
- Branches: `feat/m2-p1-identity-domain`, `feat/m2-p1-organization-domain`
- PR Target: `chore/m2-integration`

### Review Checklist
- [ ] Architecture review complete.
- [ ] Migration and test review complete.
- [ ] No drift between ADR decisions and implementation.

### Exit Criteria
- [ ] Identity and organization foundations are stable.

<a id="m2-phase-2"></a>
## Phase 2: Locations, Contacts, Academic

### Phase Goal
Implement the remaining foundation domains and validate cross-domain behavior.

### Development Checklist

#### Backend Engineering
- [ ] Implement locations updates from ADR 0008.
- [ ] Implement contacts updates from ADR 0009.
- [ ] Implement academic updates from ADR 0010.

#### QA + Testing
- [ ] Add regression tests for cross-domain constraints.

#### Docs + Standards
- [ ] Update docs for finalized cross-domain rules.

### Branch and PR Plan
- Branches: `feat/m2-p2-locations-domain`, `feat/m2-p2-contacts-domain`, `feat/m2-p2-academic-domain`
- PR Target: `chore/m2-integration`

### Review Checklist
- [ ] Model boundary and migration review complete.
- [ ] CI checks pass.
- [ ] Cross-domain references remain consistent with ADRs.

### Exit Criteria
- [ ] Domain trio is stable and test-covered.

<a id="m2-phase-3"></a>
## Phase 3: Domain Validation and Migration Freeze

### Phase Goal
Finalize domain integrity checks and freeze migration shape before access and feature milestones.

### Development Checklist

#### Backend Engineering
- [ ] Validate migration graph and reset path.

#### QA + Testing
- [ ] Finalize domain-level test pass.

#### Architecture
- [ ] Close ADR gaps or create follow-up ADR tasks.

### Branch and PR Plan
- Branch: `chore/m2-p3-domain-freeze-validation`
- PR Target: `chore/m2-integration`

### Review Checklist
- [ ] QA validation complete.
- [ ] Architecture sign-off complete.
- [ ] Milestone readiness for next dependency is confirmed.

### Exit Criteria
- [ ] Domain baseline is frozen for MVP feature work.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m2-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 3: Access and Environment Controls](./m3-access-and-environment-controls.md).
