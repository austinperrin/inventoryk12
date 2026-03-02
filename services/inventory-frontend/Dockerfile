# ==========================================================
# DEVELOPMENT IMAGE (Placeholder)
# ==========================================================
FROM node:24-alpine AS dev

ENV NODE_ENV=development
ENV PNPM_STORE_DIR=/pnpm-store

WORKDIR /repo

RUN corepack enable && corepack prepare pnpm@9.12.3 --activate

COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
COPY services/inventory-frontend/package.json services/inventory-frontend/package.json

RUN pnpm install --filter inventory-frontend

COPY services/inventory-frontend services/inventory-frontend

WORKDIR /repo/services/inventory-frontend

CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
