import { dirname } from 'node:path';
import { URL, fileURLToPath } from 'node:url';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

function normalizeBasePath(value) {
  const trimmed = value?.trim() || '/dev';

  if (!trimmed || trimmed === '/') {
    return '/';
  }

  const withLeadingSlash = trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
  return `${withLeadingSlash.replace(/\/+$/, '')}/`;
}

function normalizeRoutePath(pathname) {
  if (!pathname || pathname === '/') {
    return '/';
  }

  return pathname.replace(/\/+$/, '');
}

function installHtmlRouteGuard(devServer, basePath) {
  const normalizedBase = normalizeRoutePath(basePath);

  if (normalizedBase === '/') {
    return;
  }

  const allowedHtmlRoutes = new Set([normalizedBase, `${normalizedBase}/login`]);

  devServer.middlewares.use((request, response, next) => {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      next();
      return;
    }

    const acceptHeader = request.headers.accept || '';
    if (!acceptHeader.includes('text/html')) {
      next();
      return;
    }

    const pathname = normalizeRoutePath(new URL(request.url || '/', 'http://localhost').pathname);
    const isEnvScopedRequest =
      pathname === normalizedBase || pathname.startsWith(`${normalizedBase}/`);

    if (isEnvScopedRequest && !allowedHtmlRoutes.has(pathname)) {
      response.statusCode = 404;
      response.setHeader('Content-Type', 'text/plain; charset=utf-8');
      response.end('Not Found');
      return;
    }

    next();
  });
}

function envRouteGuardPlugin(basePath) {
  return {
    name: 'inventoryk12-env-route-guard',
    configureServer(server) {
      installHtmlRouteGuard(server, basePath);
    },
    configurePreviewServer(server) {
      installHtmlRouteGuard(server, basePath);
    },
  };
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, dirname(fileURLToPath(import.meta.url)), '');
  const basePath = normalizeBasePath(env.VITE_APP_BASE_PATH);

  return {
    base: basePath,
    plugins: [react(), envRouteGuardPlugin(basePath)],
  };
});
