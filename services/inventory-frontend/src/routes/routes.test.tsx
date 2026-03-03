import { describe, expect, it } from 'vitest';
import { appBasePath, appHomePath, appLoginPath } from './paths';
import { routes } from './routes';

describe('routes', () => {
  it('defines the baseline scaffold routes', () => {
    expect(routes.map((route) => route.id)).toEqual(['home', 'login', 'not-found']);
    expect(routes.at(-1)?.path).toBe('*');
    expect(routes.find((route) => route.id === 'home')?.path).toBe('/');
    expect(routes.find((route) => route.id === 'login')?.path).toBe('/login');
  });

  it('defaults the app path under the development environment segment', () => {
    expect(appBasePath).toBe('/dev');
    expect(appHomePath).toBe('/dev');
    expect(appLoginPath).toBe('/dev/login');
  });
});
