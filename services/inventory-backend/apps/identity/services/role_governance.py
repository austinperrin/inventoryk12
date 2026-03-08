from __future__ import annotations

from datetime import date
from typing import cast

from django.contrib.auth.models import Group, Permission
from django.db.models import Q

from apps.identity.models import RoleAssignment, User
from apps.identity.seeds import SYSTEM_MANAGED_ROLE_SEEDS
from apps.identity.services.access import resolve_user_access

SYSTEM_MANAGED_ROLE_NAMES = set(SYSTEM_MANAGED_ROLE_SEEDS)

# Guardrail baseline: never delegable through district-admin role tooling.
NON_DELEGABLE_PERMISSION_CODES = {
    "auth.add_permission",
    "auth.change_permission",
    "auth.delete_permission",
}


def is_system_managed_role(role: Group) -> bool:
    return role.name in SYSTEM_MANAGED_ROLE_NAMES


def has_active_system_admin_role(user: User, on_date: date | None = None) -> bool:
    target_date = on_date or date.today()
    return (
        RoleAssignment.objects.filter(
            user=user,
            role__name="system_admin",
            starts_on__lte=target_date,
        )
        .filter(Q(ends_on__isnull=True) | Q(ends_on__gte=target_date))
        .exists()
    )


def role_permission_codes(role: Group) -> set[str]:
    return {
        f"{app_label}.{codename}"
        for app_label, codename in role.permissions.values_list(
            "content_type__app_label",
            "codename",
        )
    }


def can_delete_role(role: Group) -> tuple[bool, str | None]:
    if is_system_managed_role(role):
        return False, "system_managed_role_protected"
    return True, None


def can_rename_role(role: Group, new_name: str) -> tuple[bool, str | None]:
    if is_system_managed_role(role) and role.name != new_name:
        return False, "system_managed_role_name_immutable"
    return True, None


def can_assign_role(
    actor: User,
    target_role: Group,
    on_date: date | None = None,
) -> tuple[bool, str | None]:
    target_codes = role_permission_codes(target_role)
    if target_codes & NON_DELEGABLE_PERMISSION_CODES:
        return False, "contains_non_delegable_permissions"

    if actor.is_superuser or has_active_system_admin_role(actor, on_date=on_date):
        return True, None

    actor_access = resolve_user_access(actor, on_date=on_date)
    if not actor_access["has_effective_access"]:
        return False, "delegator_no_effective_access"

    actor_codes = set(cast(list[str], actor_access["permissions"]))

    if not target_codes.issubset(actor_codes):
        return False, "delegation_exceeds_authority"

    return True, None


def can_grant_direct_permission(
    actor: User,
    permission: Permission,
    on_date: date | None = None,
) -> tuple[bool, str | None]:
    permission_code = f"{permission.content_type.app_label}.{permission.codename}"
    if permission_code in NON_DELEGABLE_PERMISSION_CODES:
        return False, "permission_non_delegable"

    if actor.is_superuser or has_active_system_admin_role(actor, on_date=on_date):
        return True, None

    actor_access = resolve_user_access(actor, on_date=on_date)
    if not actor_access["has_effective_access"]:
        return False, "delegator_no_effective_access"

    actor_codes = set(cast(list[str], actor_access["permissions"]))
    if permission_code not in actor_codes:
        return False, "delegation_exceeds_authority"

    return True, None
