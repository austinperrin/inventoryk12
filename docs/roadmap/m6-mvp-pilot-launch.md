# Milestone 6: MVP Pilot Launch

- Status: Not Started
- Estimate: 2-3 weeks
- Dependency: [Milestone 5: Production Deployment Readiness](./m5-production-deployment-readiness.md) `Completed`
- Related ADRs: [ADR Index](../adr/README.md) (pilot-scope relevant ADRs, including ADR 0001 through ADR 0015)

## Owners

- Milestone Owner: Product Management + TPM
- Technical Owner: DevOps + SRE
- Execution Teams: Product Management + TPM, DevOps + SRE, Security + Compliance, QA + Testing, Backend Engineering, Frontend Engineering

## Goal

Launch the production MVP pilot, support live execution, and complete pilot
exit sign-off.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] Pilot scope, success metrics, and support coverage are defined.
- [ ] Tenant onboarding checklist is finalized.
- [ ] Rollback and incident handling paths are documented.
- [ ] Pilot support and escalation ownership is documented.
- [ ] Roadmap status and owners are current.

<a id="m6-phase-1"></a>
## Phase 1: Pilot Tenant Onboarding

### Phase Goal
Onboard the pilot tenant into production with validated routing, access, and baseline configuration.

### Development Checklist

#### DevOps + SRE
- [ ] Configure tenant and environment routing.
- [ ] Provision baseline data/configuration.

#### QA + Testing
- [ ] Execute onboarding verification checklist.

### Branch and PR Plan
- Branch: `chore/m6-p1-pilot-tenant-onboarding`
- PR Target: `chore/m6-integration`

### Review Checklist
- [ ] Onboarding checklist validated.
- [ ] Security and access validation complete.
- [ ] Pilot onboarding docs match executed process.

### Exit Criteria
- [ ] Tenant is ready for live pilot workflows.

<a id="m6-phase-2"></a>
## Phase 2: Pilot Execution and Support

### Phase Goal
Operate and support live pilot usage while keeping fixes small, controlled, and traceable.

### Development Checklist

#### Product Management + TPM
- [ ] Monitor pilot usage, incidents, and support tickets.

#### Backend Engineering / Frontend Engineering
- [ ] Apply approved fixes in small PR increments.

#### Docs + Standards
- [ ] Track pilot feedback and categorize enhancement candidates.

### Branch and PR Plan
- Branch pattern: `fix/m6-p2-pilot-<topic>`
- PR Target: `chore/m6-integration`

### Review Checklist
- [ ] Support response SLAs met.
- [ ] Fixes reviewed and tested.
- [ ] Pilot feedback mapping is current and traceable.

### Exit Criteria
- [ ] Pilot runs with no unresolved critical issues.

<a id="m6-phase-3"></a>
## Phase 3: Pilot Exit and MVP Sign-Off

### Phase Goal
Close the pilot with formal acceptance, risk review, and MVP completion sign-off.

### Development Checklist

#### Product Management + TPM
- [ ] Produce pilot summary (results, defects, risks, recommendations).
- [ ] Confirm MVP acceptance criteria completion.

#### Architecture
- [ ] Open post-MVP enhancement ADR tasks where needed.

### Branch and PR Plan
- Branch: `docs/m6-p3-pilot-exit-signoff`
- PR Target: `chore/m6-integration`

### Review Checklist
- [ ] Product, QA, Security, and Ops sign-off complete.
- [ ] Remaining risks are accepted or scheduled.
- [ ] Pilot summary aligns with observed implementation behavior.

### Exit Criteria
- [ ] MVP pilot is formally accepted.
- [ ] Milestone status set to `Completed`.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 7: Post-MVP Enhancements Hook](./m7-post-mvp-enhancements.md).
