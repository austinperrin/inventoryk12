# Contributing

Thanks for your interest in contributing.

## Getting Started

1. Review `README.md` and `docs/index.md`.
2. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env --with-secrets`
3. Start local services (Docker-based):
   - `pnpm dev:up`
   - `pnpm dev:up -- --frontend`

## Principles and Workflow

- Keep changes small and reviewable.
- Update documentation alongside behavior changes.
- Follow the standards in `docs/standards/`.
- Use topic branches and open a PR for all changes, including solo work.
- Include testing evidence in PR descriptions.
- Update or add ADRs for architecture-impacting decisions.

## Required Standards

- Git workflow: `docs/standards/git-workflow.md`
- Commits: `docs/standards/commits.md`
- Reviews: `docs/standards/review.md`
- Testing: `docs/standards/testing.md`
- ADR conventions: `docs/standards/adr.md`
- AI collaboration: `docs/standards/ai-collaboration.md`

## Commits

- Follow `docs/standards/commits.md` (Conventional Commits).
