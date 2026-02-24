# Roadmap Flow v2 Proposal

- **Status**: Draft
- **Date**: 2026-02-21
- **Owners**: Product Management + TPM, Architecture, Backend Engineering, Docs + Standards

## Goal
Improve development flow by separating domain review governance from vertical
feature delivery, while keeping checklist status tied to explicit review gates.

## Why Change
- Domain implementation is proceeding faster than formal review sign-off.
- Current milestone phases mix foundation review and feature execution signals.
- AI-assisted delivery benefits from tighter review gates and smaller loops.

## Proposed Flow

### Stage A: Domain Review Loops (Governance First)
Run domain loops in planned order (`common`, `identity`, `organization`,
`locations`, `academic`, `contacts`, `enrollment`, `instruction`, `inventory`,
`operations`, `integrations`).

Per-domain loop:
1. Scope lock (domain boundaries and ownership).
2. Model + migration draft.
3. Constraint/index review.
4. ADR update for domain.
5. Review gate decision:
   - keep checklist unchecked if review is incomplete
   - check checklist only when review criteria are explicitly met

Exit criterion for Stage A:
- Required milestone domains have approved models/migrations and ADR alignment.

### Stage B: Vertical Slice Delivery (Feature First)
Once required domains are reviewed, deliver one vertical slice at a time:
1. API contract + endpoint implementation.
2. Frontend workflow implementation.
3. Integration and reporting hooks.
4. Security and audit checks.
5. Test coverage for each slice.

Exit criterion for each slice:
- Demoable flow + passing checks + doc updates.

### Stage C: Quality and Readiness Gate
1. Regression checks (backend/frontend/security).
2. Compliance evidence updates.
3. Runbook validation for real workflows.
4. Milestone review checklist closeout.

## Workflow Policy Alignment
- Local dev and operations: Docker-based (`pnpm dev:*`, `pnpm ops:* -- --docker`).
- CI checks: CI-managed dependencies in GitHub Actions (`pnpm ci:*`).
- Identifier contract: internal `id` for storage/FKs, external `uuid` for APIs.

## Suggested Board Columns
1. `Planned`
2. `In Progress`
3. `Review Pending`
4. `Blocked`
5. `Complete`

Use `Review Pending` for domain review gates before checklist status changes.

## Migration Plan From Current Roadmap
1. Keep current milestone numbering and goals.
2. Use milestone-1 Stage A domain loops as the governance gate.
3. Use milestone-1 Stage B for vertical slice execution.
4. Use milestone-1 Stage C as the readiness gate.
5. Add links from each domain checklist item to its domain ADR.

## Open Decisions
1. Minimum domain set required before first vertical slice starts.
2. Whether stage exit criteria should be enforced by automation checks.
