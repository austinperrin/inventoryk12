export function getCsrfToken(): string {
  const token = document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith('csrftoken='))
    ?.split('=')
    .slice(1)
    .join('=');

  return token ? decodeURIComponent(token) : '';
}
