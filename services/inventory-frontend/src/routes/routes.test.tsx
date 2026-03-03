import { describe, expect, it } from 'vitest';
import { routes } from './routes';

describe('routes', () => {
  it('defines the baseline scaffold routes', () => {
    expect(routes.map((route) => route.id)).toEqual(['home', 'not-found']);
    expect(routes[0]?.path).toBe('/');
    expect(routes.at(-1)?.path).toBe('*');
  });
});
