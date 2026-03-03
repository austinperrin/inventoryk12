import { apiRequest } from './api';
import { getCsrfToken } from './csrf';

export type AuthUser = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
};

type AuthEnvelope = {
  user: AuthUser;
};

type SessionEnvelope = {
  authenticated: boolean;
  user: AuthUser | null;
};

export async function primeCsrfCookie(): Promise<void> {
  await apiRequest('/api/v1/auth/csrf/');
}

export async function getSession(): Promise<SessionEnvelope> {
  return apiRequest<SessionEnvelope>('/api/v1/auth/session/');
}

export async function login(email: string, password: string): Promise<AuthUser> {
  const csrfToken = getCsrfToken();
  const data = await apiRequest<AuthEnvelope>('/api/v1/auth/login/', {
    method: 'POST',
    headers: csrfToken ? { 'X-CSRFToken': csrfToken } : undefined,
    body: { email, password },
  });

  return data.user;
}

export async function logout(): Promise<void> {
  const csrfToken = getCsrfToken();
  await apiRequest('/api/v1/auth/logout/', {
    method: 'POST',
    headers: csrfToken ? { 'X-CSRFToken': csrfToken } : undefined,
  });
}

export async function refresh(): Promise<void> {
  const csrfToken = getCsrfToken();
  await apiRequest('/api/v1/auth/refresh/', {
    method: 'POST',
    headers: csrfToken ? { 'X-CSRFToken': csrfToken } : undefined,
  });
}

export async function getCurrentUser(): Promise<AuthUser> {
  const data = await apiRequest<AuthEnvelope>('/api/v1/auth/me/');
  return data.user;
}
