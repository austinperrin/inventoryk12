# Milestone 1: Platform Baseline

- Status: Not Started
- Estimate: 2-3 weeks
- Dependency: [Milestone 0: Repository Bootstrap](./m0-repository-bootstrap.md) `Completed`
- Related ADRs: [ADR 0001](../adr/0001-tech-stack-and-runtime-baseline.md), [ADR 0002](../adr/0002-url-and-domain-topology.md)

## Owners

- Milestone Owner: Product Management + TPM
- Technical Owner: Architecture
- Execution Teams: Backend Engineering, Frontend Engineering, DevOps + SRE, Docs + Standards, QA + Testing

## Goal

Stand up backend/frontend runtime baseline and local-dev operations baseline.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] Runtime stack versions are defined and documented.
- [ ] Docker/dev workflow is documented and tested.
- [ ] API/frontend integration contracts are baseline-defined.
- [ ] Milestone branch and PR strategy is documented before implementation.
- [ ] Roadmap status and owners are current.

<a id="m1-phase-1"></a>
## Phase 1: Backend/Frontend Skeleton

### Phase Goal
Create stable backend/frontend application skeletons that can support incremental feature work.

### Development Checklist

#### Backend Engineering
- [ ] Confirm backend service skeleton and app registration structure.

#### Frontend Engineering
- [ ] Confirm frontend app shell and route scaffolding.

#### QA + Testing
- [ ] Add baseline health/status verification tests.

### Branch and PR Plan
- Branches: `feat/m1-p1-backend-skeleton`, `feat/m1-p1-frontend-skeleton`
- PR Target: `chore/m1-integration`

### Review Checklist
- [ ] Architecture and code review complete.
- [ ] Baseline tests pass.
- [ ] Skeleton implementation matches documented baseline.

### Exit Criteria
- [ ] Both services boot and pass baseline checks.

<a id="m1-phase-2"></a>
## Phase 2: Auth and Core Runtime Plumbing

### Phase Goal
Wire core authentication and runtime integration paths between backend and frontend.

### Development Checklist

#### Backend Engineering
- [ ] Wire authentication baseline flow.

#### Frontend Engineering
- [ ] Wire API client/auth guard baseline.

#### QA + Testing
- [ ] Add baseline auth integration tests.

### Branch and PR Plan
- Branch: `feat/m1-p2-auth-runtime-plumbing`
- PR Target: `chore/m1-integration`

### Review Checklist
- [ ] Security and auth review complete.
- [ ] CI checks pass.
- [ ] Auth behavior aligns with ADR and standards references.

### Exit Criteria
- [ ] Auth baseline is functional end-to-end.

<a id="m1-phase-3"></a>
## Phase 3: Local Dev + Ops Baseline

### Phase Goal
Ensure local development and operational startup flows are documented and reproducible.

### Development Checklist

#### DevOps + SRE
- [ ] Finalize docker-compose local workflow.

#### Docs + Standards
- [ ] Document startup/reset/troubleshooting commands.

#### QA + Testing
- [ ] Validate baseline runbook accuracy via smoke test.

### Branch and PR Plan
- Branch: `docs/m1-p3-local-dev-ops-baseline`
- PR Target: `chore/m1-integration`

### Review Checklist
- [ ] DevOps + Docs review complete.
- [ ] New developer smoke test passes.
- [ ] Runbooks match actual commands and expected outputs.

### Exit Criteria
- [ ] New engineer can boot stack from docs only.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m1-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 2: Domain Foundation](./m2-domain-foundation.md).
