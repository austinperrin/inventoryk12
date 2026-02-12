# API Standards

## Versioning

- All endpoints are versioned under `/api/v1/`.

## Naming

- Use plural nouns for resources: `/assets/`, `/districts/`.
- Use kebab-case or snake_case consistently in URLs (pick one when implementing).

## Errors

- Use a consistent error response shape:
  - `error.code` (string, stable identifier)
  - `error.message` (human-readable summary)
  - `error.details` (optional, list or object with field-level info)
  - `error.request_id` (optional, for tracing)

Example:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request payload.",
    "details": {
      "serial": ["This field is required."]
    },
    "request_id": "req_123"
  }
}
```

## Pagination

- Use limit/offset pagination consistently across list endpoints.
- Request params: `limit`, `offset`
- Response fields: `count`, `next`, `previous`, `results`

Example:
```json
{
  "count": 125,
  "next": "/api/v1/assets/?limit=25&offset=25",
  "previous": null,
  "results": []
}
```

## Authentication Endpoints (MVP)

- `POST /api/v1/auth/login/` (email/password -> access/refresh tokens)
- `POST /api/v1/auth/refresh/` (refresh token -> new access token)
- `POST /api/v1/auth/logout/` (invalidate refresh token)
- `GET /api/v1/auth/me/` (current user profile)
