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

- [ ] `docs/index.md` and `docs/roadmap/index.md` are aligned.
- [ ] Branch, commit, and PR standards are confirmed and current.
- [ ] CI quality gates and required checks are defined.
- [ ] ADR references for technical decisions are listed and valid.
- [ ] Current milestone status in roadmap index matches actual execution state.

<a id="m0-phase-1"></a>
## Phase 1: Repo Scaffold and Guardrails

### Phase Goal
Establish the minimum repo structure and safety rails required for consistent delivery.

### Development Checklist

#### Docs + Standards
- [ ] Confirm monorepo top-level structure documentation for services, infra, configs, docs.

#### Backend Engineering
- [ ] Add/update baseline backend tooling configuration files.

#### DevOps + SRE
- [ ] Ensure protected branch and required-check expectations are documented.

### Branch and PR Plan
- Branch: `chore/m0-p1-repo-scaffold-guardrails`
- PR Target: `chore/m0-integration`

### Review Checklist
- [ ] Repo structure and conventions reviewed.
- [ ] Standards references are correct.
- [ ] No undocumented structural drift introduced.

### Exit Criteria
- [ ] Baseline structure and guardrails are merged.

<a id="m0-phase-2"></a>
## Phase 2: Standards and Workflow Wiring

### Phase Goal
Align working standards, templates, and process guidance so day-to-day execution is predictable.

### Development Checklist

#### Docs + Standards
- [ ] Finalize commit/branch/PR standards references.
- [ ] Add missing docs links to avoid process ambiguity.

#### DevOps + SRE
- [ ] Validate checklist/template alignment with `.github` workflows/templates.

### Branch and PR Plan
- Branch: `docs/m0-p2-standards-workflow-wiring`
- PR Target: `chore/m0-integration`

### Review Checklist
- [ ] Docs + standards review complete.
- [ ] Junior-dev workflow is clear and executable.
- [ ] Workflow docs match actual repository automation.

### Exit Criteria
- [ ] Standards and workflow docs are consistent and usable.

<a id="m0-phase-3"></a>
## Phase 3: Baseline CI and Quality Gate

### Phase Goal
Stand up baseline CI checks and ownership so quality gates are enforceable from the start.

### Development Checklist

#### DevOps + SRE
- [ ] Define required CI checks for docs, lint, and tests.
- [ ] Validate minimal green pipeline for baseline repo state.

#### Product Management + TPM
- [ ] Define failure ownership and triage flow.

### Branch and PR Plan
- Branch: `ci/m0-p3-baseline-quality-gates`
- PR Target: `chore/m0-integration`

### Review Checklist
- [ ] CI checks pass.
- [ ] Failure-handling guidance is documented.
- [ ] Required quality gates are enforced and visible.

### Exit Criteria
- [ ] Baseline quality gate is operational.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m0-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 1: Platform Baseline](./m1-platform-baseline.md).
