const rawBasePath = import.meta.env.VITE_APP_BASE_PATH?.trim() || '/dev';

function normalizeBasePath(value: string): string {
  const trimmed = value.trim();

  if (!trimmed || trimmed === '/') {
    return '/';
  }

  const withLeadingSlash = trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
  return withLeadingSlash.replace(/\/+$/, '');
}

function joinPath(basePath: string, childPath: string): string {
  if (childPath === '/') {
    return basePath;
  }

  return basePath === '/' ? childPath : `${basePath}${childPath}`;
}

export const appBasePath = normalizeBasePath(rawBasePath);
export const routeHomePath = '/';
export const routeLoginPath = '/login';
export const appHomePath = joinPath(appBasePath, routeHomePath);
export const appLoginPath = joinPath(appBasePath, routeLoginPath);
