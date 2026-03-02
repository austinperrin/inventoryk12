# Documentation Guidelines

## Scope
- Applies to `docs/**`. Follow this file instead of the repo root guidance when they overlap.

## Structure
- Treat `docs/index.md` as the documentation entrypoint.
- Roadmap sequencing and execution status belong in `docs/roadmap/`; `docs/roadmap/index.md` is the canonical schedule view.
- Architectural decisions belong in `docs/adr/`; update an ADR or add a new one when a repo-wide technical decision changes.
- Standards and guardrails belong in `docs/standards/`; keep those aligned with actual repo behavior, not aspirational process.

## Writing Conventions
- Keep docs specific to this repo. Prefer concrete file paths, commands, milestone names, and ADR references.
- Preserve the scaffold-first status of the project. Do not document domains, infrastructure, or security controls as implemented unless the code and workflows already support them.
- When a behavior change affects developer workflow, CI, security posture, or service boundaries, update the closest doc instead of leaving the change implicit.

## ADR and Roadmap Rules
- Before changing runtime, auth, deployment, storage, or worker assumptions, check `docs/adr/0001-tech-stack-and-runtime-baseline.md`.
- Keep roadmap dates, milestones, and status fields internally consistent when editing `docs/roadmap/`.
- Use `docs/adr/template.md` for new ADRs and keep related ADR links current in `docs/adr/README.md` when the set expands materially.
