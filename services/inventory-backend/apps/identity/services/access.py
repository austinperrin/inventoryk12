from __future__ import annotations

from datetime import date

from django.contrib.auth.models import Permission
from django.db.models import Q
from django.utils import timezone

from apps.identity.models import RoleAssignment, User


def resolve_user_access(user: User, on_date: date | None = None) -> dict[str, object]:
    target_date = on_date or timezone.localdate()

    active_role_ids = list(
        RoleAssignment.objects.filter(user=user, starts_on__lte=target_date)
        .filter(Q(ends_on__isnull=True) | Q(ends_on__gte=target_date))
        .values_list("role_id", flat=True)
        .distinct()
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
    has_effective_access = user.is_superuser or bool(permission_codes)
    access_outcome = "granted" if has_effective_access else "no_access"

    return {
        "has_effective_access": has_effective_access,
        "access_outcome": access_outcome,
        "permissions": permission_codes,
    }
