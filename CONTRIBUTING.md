# Contributing

Thanks for your interest in contributing.

## Getting Started

1. Review `README.md` and `docs/index.md`.
2. Create env files:
   - `pnpm bootstrap:env`
   - `pnpm bootstrap:env -- --with-secrets`
3. Start local services (Docker-based):
   - `pnpm dev:up`
   - `pnpm dev:up -- --frontend`
4. Apply backend migrations:
   - `pnpm ops:migrate -- --docker`
5. Follow the local smoke-test and troubleshooting runbook:
   - `docs/runbooks/local-development.md`

## Principles and Workflow

- Keep changes small and reviewable.
- Update documentation alongside behavior changes.
- Follow the standards in `docs/standards/`.
- Use topic branches and open a PR for all changes, including solo work.
- Include testing evidence in PR descriptions.
- Update or add ADRs for architecture-impacting decisions.
- Use `.github/overview.md` and the matching PR template when workflow or CI
  expectations are involved.

## Required Standards

- Commits: `docs/standards/commits.md`
- Coding standards: `docs/standards/coding-standards.md`
- Testing: `docs/standards/testing.md`
- ADR conventions: `docs/standards/adr.md`
- Security standards: `docs/standards/security.md`
- Script standards: `docs/standards/scripts.md`

## Commits

- Follow `docs/standards/commits.md` (Conventional Commits).
