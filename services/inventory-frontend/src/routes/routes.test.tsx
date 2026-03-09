import { describe, expect, it } from 'vitest';
import { appBasePath, appHomePath, appLoginPath, appNoAccessPath } from './paths';
import { routes } from './routes';

describe('routes', () => {
  it('defines the baseline scaffold routes', () => {
    expect(routes.map((route) => route.id)).toEqual(['home', 'login', 'no-access', 'not-found']);
    expect(routes.at(-1)?.path).toBe('*');
    expect(routes.find((route) => route.id === 'home')?.path).toBe('/');
    expect(routes.find((route) => route.id === 'login')?.path).toBe('/login');
    expect(routes.find((route) => route.id === 'no-access')?.path).toBe('/no-access');
  });

  it('defaults the app path under the development environment segment', () => {
    expect(appBasePath).toBe('/dev');
    expect(appHomePath).toBe('/dev');
    expect(appLoginPath).toBe('/dev/login');
    expect(appNoAccessPath).toBe('/dev/no-access');
  });
});
