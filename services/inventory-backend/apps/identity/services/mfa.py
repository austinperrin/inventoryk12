from __future__ import annotations

import secrets
from datetime import date
from uuid import uuid4

from django.conf import settings
from django.core import signing
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Q

from apps.identity.models import MfaPolicy, RoleAssignment, User

MFA_CHALLENGE_CACHE_PREFIX = "identity:mfa:challenge:"


def get_or_create_mfa_policy() -> MfaPolicy:
    policy, _ = MfaPolicy.objects.get_or_create(policy_key="default")
    return policy


def mfa_policy_summary() -> dict[str, object]:
    policy = get_or_create_mfa_policy()
    return {
        "enforce_for_all": bool(policy.enforce_for_all),
        "allow_user_opt_in": bool(policy.allow_user_opt_in),
        "enforced_role_names": sorted(policy.enforced_roles.values_list("name", flat=True)),
    }


def requires_mfa_for_user(user: User, on_date: date | None = None) -> bool:
    target_date = on_date or date.today()
    policy = get_or_create_mfa_policy()

    if policy.enforce_for_all:
        return True

    active_role_names = set(
        RoleAssignment.objects.filter(
            user=user,
            starts_on__lte=target_date,
        )
        .filter(Q(ends_on__isnull=True) | Q(ends_on__gte=target_date))
        .values_list("role__name", flat=True)
    )
    if "system_admin" in active_role_names:
        return True

    enforced_role_names = set(policy.enforced_roles.values_list("name", flat=True))
    if active_role_names & enforced_role_names:
        return True

    return bool(policy.allow_user_opt_in and user.mfa_enabled)


def issue_mfa_challenge(user: User) -> str:
    challenge_id = str(uuid4())
    code = "".join(secrets.choice("0123456789") for _ in range(6))
    cache.set(
        f"{MFA_CHALLENGE_CACHE_PREFIX}{challenge_id}",
        {"user_id": str(user.pk), "code": code},
        timeout=int(settings.AUTH_MFA_CHALLENGE_TTL_SECONDS),
    )
    send_mail(
        subject="InventoryK12 verification code",
        message=f"Your verification code is: {code}",
        from_email=None,
        recipient_list=[user.email],
        fail_silently=True,
    )
    return challenge_id


def verify_mfa_challenge(user: User, challenge_id: str, code: str) -> bool:
    cache_key = f"{MFA_CHALLENGE_CACHE_PREFIX}{challenge_id}"
    payload = cache.get(cache_key)
    if not payload:
        return False
    if str(payload.get("user_id")) != str(user.pk):
        return False
    if str(payload.get("code")) != code.strip():
        return False

    cache.delete(cache_key)
    return True


def issue_mfa_cookie_value(user: User) -> str:
    return signing.dumps({"user_id": user.pk}, salt=settings.AUTH_MFA_COOKIE_SALT)


def has_recent_mfa_cookie(cookie_value: str | None, user: User) -> bool:
    if not cookie_value:
        return False

    try:
        payload = signing.loads(
            cookie_value,
            salt=settings.AUTH_MFA_COOKIE_SALT,
            max_age=int(settings.AUTH_MFA_RECENT_WINDOW_SECONDS),
        )
    except signing.BadSignature:
        return False
    except signing.SignatureExpired:
        return False

    return str(payload.get("user_id")) == str(user.pk)
