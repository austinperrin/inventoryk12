export class ApiError extends Error {
  status: number;
  data: unknown;
  retryAfterSeconds: number | null;

  constructor(message: string, status: number, data: unknown, retryAfterSeconds: number | null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
    this.retryAfterSeconds = retryAfterSeconds;
  }
}

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim() || 'http://127.0.0.1:8000';

export const apiBaseUrl = rawBaseUrl.replace(/\/+$/, '');

type RequestOptions = RequestInit & {
  body?: BodyInit | null | object;
};

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers = new Headers(options.headers);
  let body = options.body;

  if (body && typeof body === 'object' && !(body instanceof FormData) && !(body instanceof URLSearchParams)) {
    headers.set('Content-Type', 'application/json');
    body = JSON.stringify(body);
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    credentials: 'include',
    ...options,
    headers,
    body,
  });

  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : await response.text();
  const retryAfterHeader = response.headers.get('Retry-After');
  const retryAfterSeconds =
    retryAfterHeader && Number.isFinite(Number.parseInt(retryAfterHeader, 10))
      ? Number.parseInt(retryAfterHeader, 10)
      : null;

  if (!response.ok) {
    throw new ApiError(
      `Request failed with status ${response.status}`,
      response.status,
      data,
      retryAfterSeconds,
    );
  }

  return data as T;
}
