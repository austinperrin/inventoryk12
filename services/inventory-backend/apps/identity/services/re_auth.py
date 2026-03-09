from __future__ import annotations

from django.conf import settings
from django.core import signing

from apps.identity.models import User


def issue_reauth_cookie_value(user: User) -> str:
    return signing.dumps(
        {"user_id": user.pk},
        salt=settings.AUTH_REAUTH_COOKIE_SALT,
    )


def has_recent_reauth_cookie(cookie_value: str | None, user: User) -> bool:
    if not cookie_value:
        return False

    try:
        payload = signing.loads(
            cookie_value,
            salt=settings.AUTH_REAUTH_COOKIE_SALT,
            max_age=int(settings.AUTH_REAUTH_WINDOW_SECONDS),
        )
    except signing.BadSignature:
        return False
    except signing.SignatureExpired:
        return False

    return str(payload.get("user_id")) == str(user.pk)
