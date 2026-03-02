# Milestone 0: Repository Bootstrap

- Status: In Progress
- Estimate: 1-2 weeks
- Dependencies: none
- Related ADRs: [ADR 0001](../adr/0001-tech-stack-and-runtime-baseline.md)

## Owners

- Milestone Owner: Product Management + TPM
- Technical Owner: Architecture
- Execution Teams: Docs + Standards, DevOps + SRE, Backend Engineering

## Goal

Create a clean, enforceable repository baseline so all later milestones execute in
small, predictable branch/PR increments.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [x] `docs/index.md` and `docs/roadmap/index.md` are aligned.
- [x] Branch, commit, and PR standards are confirmed and current.
- [x] CI quality gates and required checks are defined.
- [x] ADR references for technical decisions are listed and valid.
- [x] Current milestone status in roadmap index matches actual execution state.

## Execution Model

- Milestone pre-checklist updates should be completed on the milestone branch
  `chore/m0-integration`.
- Each phase branch should be created from `chore/m0-integration`.
- Each phase should be completed on its recommended phase branch.
- Phase-specific checklist and status updates should be committed in that same
  phase branch instead of being deferred.
- Each phase branch should merge back into `chore/m0-integration` after that
  phase is complete.
- The milestone branch `chore/m0-integration` is reserved for milestone-level
  reconciliation, milestone review checklist updates, and the final PR to `main`.

<a id="m0-phase-1"></a>
## Phase 1: Repo Scaffold and Guardrails

### Phase Goal
Establish the minimum repo structure and safety rails required for consistent delivery.

### Development Checklist

#### Docs + Standards
- [x] Confirm monorepo top-level structure documentation for services, infra, configs, docs.

#### Backend Engineering
- [x] Add/update baseline backend tooling configuration files.

#### DevOps + SRE
- [x] Ensure protected branch and required-check expectations are documented.

### Branch and PR Plan
- Branch: `chore/m0-p1-repo-scaffold-guardrails`
- PR Target: `chore/m0-integration`

### Review Checklist
- [x] Repo structure and conventions reviewed.
- [x] Standards references are correct.
- [x] No undocumented structural drift introduced.

### Exit Criteria
- [x] Phase 1 deliverables and checklist updates are ready to merge into `chore/m0-integration`.

<a id="m0-phase-2"></a>
## Phase 2: Standards and Workflow Wiring

### Phase Goal
Align working standards, templates, and process guidance so day-to-day execution is predictable.

### Development Checklist

#### Docs + Standards
- [x] Finalize commit/branch/PR standards references.
- [x] Add missing docs links to avoid process ambiguity.

#### DevOps + SRE
- [x] Validate checklist/template alignment with `.github` workflows/templates.

### Branch and PR Plan
- Branch: `docs/m0-p2-standards-workflow-wiring`
- PR Target: `chore/m0-integration`

### Review Checklist
- [x] Docs + standards review complete.
- [x] Junior-dev workflow is clear and executable.
- [x] Workflow docs match actual repository automation.

### Exit Criteria
- [x] Phase 2 deliverables and checklist updates are ready to merge into `chore/m0-integration`.

<a id="m0-phase-3"></a>
## Phase 3: Baseline CI and Quality Gate

### Phase Goal
Stand up baseline CI checks and ownership so quality gates are enforceable from the start.

### Development Checklist

#### DevOps + SRE
- [x] Define required CI checks for docs, lint, and tests.
- [ ] Validate minimal green pipeline for baseline repo state.

#### Product Management + TPM
- [x] Define failure ownership and triage flow.

### Branch and PR Plan
- Branch: `ci/m0-p3-baseline-quality-gates`
- PR Target: `chore/m0-integration`

### Review Checklist
- [ ] CI checks pass.
- [x] Failure-handling guidance is documented.
- [ ] Required quality gates are enforced and visible.

### Exit Criteria
- [ ] Phase 3 deliverables and checklist updates are ready to merge into `chore/m0-integration`.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m0-integration` contains the merged output from all milestone phase branches.
- [ ] Milestone review checklist updates are committed on `chore/m0-integration`.
- [ ] `chore/m0-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 1: Platform Baseline](./m1-platform-baseline.md).
