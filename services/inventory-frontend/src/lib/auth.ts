import { ApiError, apiRequest } from './api';
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

export async function primeCsrfCookie(): Promise<void> {
  try {
    await apiRequest<AuthEnvelope>('/api/v1/auth/me/');
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      return;
    }
    throw error;
  }
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
