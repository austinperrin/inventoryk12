# Frontend

Vite + React + TypeScript frontend for InventoryK12.

## Structure

- `src/main.tsx` bootstraps the React app.
- `src/App.tsx` owns the top-level app shell and route mounting.
- `src/routes/routes.tsx` defines the typed route scaffold for milestone-driven expansion.
- `src/pages/` contains page-level UI for the current route map.
- `src/routes/routes.test.tsx` provides a baseline route-shape check for the scaffold.

## Scripts

- `pnpm dev`
- `pnpm build`
- `pnpm test`

## TypeScript

TypeScript is enabled via `tsconfig.json` and `tsconfig.node.json`.
