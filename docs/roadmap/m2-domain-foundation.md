# Milestone 2: Domain Foundation

- Status: Not Started
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

- [ ] Domain order is dependency-aligned.
- [ ] Each domain task is PR-sized and branch-planned.
- [ ] ADR links for each domain are explicit and current.
- [ ] Migration review and rollback approach is documented.
- [ ] Roadmap status and owners are current.

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
