from __future__ import annotations

from datetime import date

from django.contrib.auth.models import Permission
from django.db.models import Q
from django.utils import timezone

from apps.identity.models import RoleAssignment, RoleLoginLock, User, UserLoginLock

DEFAULT_NO_ACCESS_MESSAGES = {
    "login_locked": "Your account is currently locked. Contact your administrator.",
    "not_verified": "Your account is not verified yet. Contact your administrator.",
    "require_password_reset": "You must reset your password before continuing.",
    "no_effective_permissions": (
        "Your account is active but has no effective permissions assigned."
    ),
}


def resolve_user_access(user: User, on_date: date | None = None) -> dict[str, object]:
    target_date = on_date or timezone.localdate()
    now = timezone.now()

    active_role_ids = list(
        RoleAssignment.objects.filter(user=user, starts_on__lte=target_date)
        .filter(Q(ends_on__isnull=True) | Q(ends_on__gte=target_date))
        .values_list("role_id", flat=True)
        .distinct()
    )
    has_active_role_assignment = bool(active_role_ids)

    active_user_locks = UserLoginLock.objects.filter(user=user, starts_at__lte=now).filter(
        Q(ends_at__isnull=True) | Q(ends_at__gte=now)
    )
    active_role_locks = RoleLoginLock.objects.filter(
        role_id__in=active_role_ids,
        starts_at__lte=now,
    ).filter(Q(ends_at__isnull=True) | Q(ends_at__gte=now))

    has_active_user_lock = active_user_locks.exists()
    has_active_role_lock = active_role_locks.exists()
    has_active_login_lock = has_active_user_lock or has_active_role_lock

    user_lock_reason = (
        active_user_locks.exclude(reason="")
        .order_by("-starts_at")
        .values_list("reason", flat=True)
        .first()
    )
    role_lock_reason = (
        active_role_locks.exclude(reason="")
        .order_by("-starts_at")
        .values_list("reason", flat=True)
        .first()
    )

    role_permission_codes = {
        f"{app_label}.{codename}"
        for app_label, codename in Permission.objects.filter(group__id__in=active_role_ids)
        .values_list("content_type__app_label", "codename")
        .distinct()
    }
    direct_permission_codes = {
        f"{app_label}.{codename}"
        for app_label, codename in user.user_permissions.values_list(
            "content_type__app_label",
            "codename",
        )
    }

    permission_codes = sorted(role_permission_codes | direct_permission_codes)
    has_any_permissions = user.is_superuser or bool(permission_codes)
    no_access_reason = None
    if has_active_login_lock:
        no_access_reason = "login_locked"
    elif user.verified_at is None:
        no_access_reason = "not_verified"
    elif user.require_password_reset:
        no_access_reason = "require_password_reset"
    elif not has_any_permissions:
        no_access_reason = "no_effective_permissions"

    has_effective_access = no_access_reason is None
    access_outcome = "granted" if has_effective_access else "no_access"
    no_access_message = None
    if no_access_reason is not None:
        if no_access_reason == "login_locked":
            no_access_message = user_lock_reason or role_lock_reason
        if not no_access_message:
            no_access_message = DEFAULT_NO_ACCESS_MESSAGES[no_access_reason]

    return {
        "has_effective_access": has_effective_access,
        "access_outcome": access_outcome,
        "no_access_reason": no_access_reason,
        "no_access_message": no_access_message,
        "has_active_role_assignment": has_active_role_assignment,
        "has_direct_permissions": bool(direct_permission_codes),
        "has_active_login_lock": has_active_login_lock,
        "is_verified": user.verified_at is not None,
        "permissions": permission_codes,
    }
