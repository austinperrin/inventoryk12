# Coding Standards

This document defines coding rules for the codebase. If a rule conflicts with
linting/formatting tools, tools take precedence.

## General

- Keep modules small and focused.
- Prefer explicit names over abbreviations.
- Avoid side effects in module import time.
- Keep functions under ~50 lines when possible.
- Document any non-obvious behavior inline with short comments.

## Python / Django

- Follow `ruff`, `black`, and `isort` defaults.
- Use type hints for function signatures.
- Avoid circular imports; use local imports if needed.
- Prefer service functions over fat model methods.
- Avoid raw SQL unless necessary and documented.

## TypeScript / React

- Use TypeScript for all new frontend code.
- Prefer functional components.
- Keep components small and composable.
- Avoid inline styles unless necessary; use CSS modules or scoped styles.
- Prefer typed props over `any`.

## Formatting

- Run `pnpm dev:format` before PRs.
- The CI pipeline enforces formatting.
