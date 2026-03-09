from __future__ import annotations

from datetime import datetime

from django.conf import settings

SESSION_STARTED_AT_CLAIM = "ik12_session_started_at"
LAST_ACTIVITY_AT_CLAIM = "ik12_last_activity_at"


def _claim_value(token: object, claim: str, fallback: int) -> int:
    payload = getattr(token, "payload", None)
    if isinstance(payload, dict):
        value = payload.get(claim, fallback)
    else:
        value = fallback
        try:
            value = token[claim]  # type: ignore[index]
        except Exception:
            value = fallback
    return int(value)


def add_session_claims(refresh_token: object, *, now: datetime) -> None:
    now_ts = int(now.timestamp())
    session_started_at = _claim_value(refresh_token, SESSION_STARTED_AT_CLAIM, now_ts)
    refresh_token[SESSION_STARTED_AT_CLAIM] = session_started_at  # type: ignore[index]
    refresh_token[LAST_ACTIVITY_AT_CLAIM] = now_ts  # type: ignore[index]


def validate_session_window(
    refresh_token: object, *, now: datetime
) -> tuple[bool, str | None]:
    now_ts = int(now.timestamp())
    session_started_at = _claim_value(refresh_token, SESSION_STARTED_AT_CLAIM, now_ts)
    last_activity_at = _claim_value(refresh_token, LAST_ACTIVITY_AT_CLAIM, now_ts)

    absolute_lifetime = int(settings.AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS)
    idle_timeout = int(settings.AUTH_SESSION_IDLE_TIMEOUT_SECONDS)

    if now_ts - session_started_at >= absolute_lifetime:
        return False, "session_absolute_timeout"
    if now_ts - last_activity_at >= idle_timeout:
        return False, "session_idle_timeout"

    return True, None
