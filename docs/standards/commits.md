# Commit Standards

We use Conventional Commits to keep history readable and enable automation.

## Format

`<type>(<scope>): <subject>`

Examples:

- `chore(repo): scaffold initial tooling`
- `docs(standards): add commit conventions`
- `feat(inventory): add asset import endpoint`
- `fix(inventory-ui): handle empty search results`

## Types

- `feat` new user-facing functionality
- `fix` bug fixes
- `docs` documentation only
- `style` formatting only (no logic)
- `refactor` code change without new behavior
- `test` add or update tests
- `chore` tooling, build, or maintenance
- `perf` performance improvements
- `ci` CI configuration changes
- `build` build system changes

## Rules

- Use present tense in the subject.
- Keep the subject under 72 characters.
- Use a clear scope for product or area (e.g., `inventory`, `repo`, `docs`).

## Granularity

- Keep each commit focused on a single concern.
- Do not mix unrelated changes in one commit (for example, feature work + refactor + docs cleanup).
- Prefer multiple small commits over one large mixed commit.
- If behavior changes, include tests and docs updates in the same PR; keep commits logically grouped.

## Branch Naming

Use:

`<type>/<scope>-<short-description>`

Branch naming rules:
- Use lowercase only.
- Use hyphens in the description.
- Keep names short and specific to one unit of work.
- Match `type` to Conventional Commit intent when possible.

Common types:
- `feat`
- `fix`
- `docs`
- `chore`
- `refactor`
- `test`
- `ci`

Examples:
- `feat/inventory-checkout-flow`
- `fix/inventory-audit-reconciliation-bug`
- `docs/roadmap-m0-phase1-adr-update`
- `chore/repo-ci-backend-typecheck`
- `test/inventory-auth-unit-coverage`

Milestone/phase example:
- `docs/roadmap-m0-p1-finalize-adr-0002`

## PR Merge Strategy

- Use squash merge for pull requests into `main`.
- Before merging, edit the squash commit message to follow Conventional Commit format.
- Ensure the final squash commit clearly describes the shipped change set, not intermediate WIP steps.

## Issue and Ticket Linking

Use footers in commit messages and PR descriptions:

- `Refs #123` for related work
- `Closes #123` when the change resolves the issue

Examples:
- `feat(inventory): add assignment export endpoint`
  - `Refs #142`
- `fix(inventory-ui): handle empty audit results`
  - `Closes #187`

## Enforcement

Local commits are enforced via `husky` + `commitlint`.
Run `pnpm install` to install hooks after cloning.
