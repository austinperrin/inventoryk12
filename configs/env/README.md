# Environment Files

This directory contains example environment files used to create local `.env` files.

## Files

- `.env.backend.example` template for backend services
- `.env.frontend.example` template for frontend services

## Usage

Use the bootstrap script to create local env files:

- `pnpm bootstrap:env`
- `pnpm bootstrap:env -- --with-secrets`
- Rotate backend secret on demand: `pnpm bootstrap:secrets -- --force`

## Policy

- Never commit real secrets to version control.
- Keep `.env` files local and out of git.
- Update examples when new configuration is required.
- Local and production runtimes are expected to run in Docker/containerized environments.
