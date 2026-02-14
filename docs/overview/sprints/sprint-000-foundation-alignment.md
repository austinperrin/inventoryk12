# Sprint 000: Foundation Alignment

- **Sprint ID**: Sprint 000
- **Dates**: 2026-02-13 to 2026-02-13
- **Milestone**: Milestone 0 (Foundation Alignment)
- **Owners**: Product Management + TPM, Architecture, Backend Engineering, Docs + Standards
- **Status**: Complete

## Scope

- Align repo standards, runbooks, ADR format, and roadmap tracking.
- Finalize ADR 0002 as incremental modeling strategy.
- Resolve pre-development consistency gaps across docs and scripts.

## Sprint-0 Risk Log

| Risk | Owner | Trigger | Mitigation | Status |
| --- | --- | --- | --- | --- |
| Docs drift while standards are still evolving | Docs + Standards | New standards or file moves without index updates | Keep `docs/index.md` synchronized; include docs checks in PR templates | Mitigated |
| Over-scoping before first implementation sprint | Product Management + TPM | New feature asks bypass roadmap gates | Keep candidate ideas in `docs/overview/feature-candidates.md`; commit scope via roadmap tasks | Mitigated |
| Script/runbook mismatch causing onboarding friction | DevOps + SRE | Commands in docs differ from executable scripts | Keep runbooks tied to `pnpm` scripts and validate shell syntax | Mitigated |
| Model lock-in too early | Architecture | Schema is over-defined before implementation feedback | Use ADR 0002 incremental strategy and follow-up ADRs per domain | Mitigated |

## Board and Workflow

- Milestone board model: `Planned -> In Progress -> Complete` (with `Blocked` as exception state).
- Work unit mapping: roadmap milestone and phase checklist items.
- Review cadence: weekly planning/review, with milestone review checklist at phase close.

## Evidence of Completion

- ADR updates completed:
  - `docs/adr/0001-auth-strategy.md`
  - `docs/adr/0002-core-data-model.md`
  - `docs/adr/0003-ingestion-architecture.md`
  - `docs/adr/template.md`
- Standards and workflow updates completed:
  - `docs/standards/adr.md`
  - `docs/standards/git-workflow.md`
  - `docs/standards/testing.md`
  - `docs/standards/review.md`
- Runbooks and architecture baseline updated:
  - `docs/runbooks/deploy.md`
  - `docs/runbooks/incident-response.md`
  - `docs/architecture/README.md`
- Scripts aligned and non-placeholder operations baseline implemented under `scripts/`.

## Notes

- Issue/PR state is tracked in this sprint record and roadmap during pre-issue-bootstrap phase.
- Future sprints should move status tracking to issue board artifacts once project boards are fully configured.
