from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils import timezone

from apps.identity.models import RoleAssignment
from apps.identity.services.role_governance import (
    can_assign_role,
    can_delete_role,
    can_grant_direct_permission,
    can_rename_role,
    has_active_system_admin_role,
    is_system_managed_role,
)

User = get_user_model()


def _user(email: str):
    return User.objects.create_user(
        email=email,
        password="ChangeMe123!",
        verified_at=timezone.now(),
    )


@pytest.mark.django_db
def test_system_managed_role_detection_and_protection() -> None:
    seeded_role = Group.objects.create(name="teacher")
    custom_role = Group.objects.create(name="custom-campus-role")

    assert is_system_managed_role(seeded_role) is True
    assert is_system_managed_role(custom_role) is False
    assert can_delete_role(seeded_role) == (False, "system_managed_role_protected")
    assert can_delete_role(custom_role) == (True, None)
    assert can_rename_role(seeded_role, "teacher") == (True, None)
    assert can_rename_role(seeded_role, "teacher-v2") == (
        False,
        "system_managed_role_name_immutable",
    )


@pytest.mark.django_db
def test_role_assignment_delegation_requires_subset_of_actor_permissions() -> None:
    actor = _user("actor@example.com")
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    actor_role = Group.objects.create(name="site_admin_actor")
    actor_role.permissions.add(view_group_permission)
    RoleAssignment.objects.create(
        user=actor,
        role=actor_role,
        starts_on=timezone.localdate(),
    )

    allowed_target = Group.objects.create(name="teacher_allowed")
    allowed_target.permissions.add(view_group_permission)
    denied_target = Group.objects.create(name="teacher_denied")
    denied_target.permissions.add(
        Permission.objects.get(
            content_type__app_label="auth",
            codename="add_group",
        )
    )

    assert can_assign_role(actor, allowed_target) == (True, None)
    assert can_assign_role(actor, denied_target) == (False, "delegation_exceeds_authority")


@pytest.mark.django_db
def test_role_assignment_delegation_denies_non_delegable_permissions() -> None:
    actor = _user("guardrail@example.com")
    actor_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="change_permission",
    )
    actor_role = Group.objects.create(name="district_admin_actor")
    actor_role.permissions.add(actor_permission)
    RoleAssignment.objects.create(
        user=actor,
        role=actor_role,
        starts_on=timezone.localdate(),
    )

    target_role = Group.objects.create(name="sensitive-role")
    target_role.permissions.add(actor_permission)

    assert can_assign_role(actor, target_role) == (
        False,
        "contains_non_delegable_permissions",
    )


@pytest.mark.django_db
def test_role_assignment_delegation_denies_when_actor_has_no_effective_access() -> None:
    actor = _user("expired@example.com")
    permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    actor_role = Group.objects.create(name="expired-role")
    actor_role.permissions.add(permission)
    today = timezone.localdate()
    RoleAssignment.objects.create(
        user=actor,
        role=actor_role,
        starts_on=today - timedelta(days=2),
        ends_on=today - timedelta(days=1),
    )
    target_role = Group.objects.create(name="target-role")
    target_role.permissions.add(permission)

    assert can_assign_role(actor, target_role) == (False, "delegator_no_effective_access")


@pytest.mark.django_db
def test_system_admin_role_assignment_has_district_superuser_authority() -> None:
    actor = _user("district-super@example.com")
    system_admin_role = Group.objects.create(name="system_admin")
    RoleAssignment.objects.create(
        user=actor,
        role=system_admin_role,
        starts_on=timezone.localdate(),
    )
    target_role = Group.objects.create(name="teacher-target")
    target_role.permissions.add(
        Permission.objects.get(
            content_type__app_label="auth",
            codename="add_group",
        )
    )

    assert has_active_system_admin_role(actor) is True
    assert can_assign_role(actor, target_role) == (True, None)


@pytest.mark.django_db
def test_system_admin_still_respects_non_delegable_permission_guardrails() -> None:
    actor = _user("district-super-guardrail@example.com")
    RoleAssignment.objects.create(
        user=actor,
        role=Group.objects.create(name="system_admin"),
        starts_on=timezone.localdate(),
    )
    target_role = Group.objects.create(name="sensitive-role")
    target_role.permissions.add(
        Permission.objects.get(
            content_type__app_label="auth",
            codename="change_permission",
        )
    )

    assert can_assign_role(actor, target_role) == (
        False,
        "contains_non_delegable_permissions",
    )


@pytest.mark.django_db
def test_system_admin_role_assignment_can_grant_direct_permissions() -> None:
    actor = _user("district-super-direct@example.com")
    RoleAssignment.objects.create(
        user=actor,
        role=Group.objects.create(name="system_admin"),
        starts_on=timezone.localdate(),
    )
    permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="add_group",
    )

    assert can_grant_direct_permission(actor, permission) == (True, None)


@pytest.mark.django_db
def test_direct_permission_grant_checks_follow_authority_and_guardrails() -> None:
    actor = _user("direct-grant@example.com")
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    actor_role = Group.objects.create(name="direct-grant-role")
    actor_role.permissions.add(view_group_permission)
    RoleAssignment.objects.create(
        user=actor,
        role=actor_role,
        starts_on=timezone.localdate(),
    )

    assert can_grant_direct_permission(actor, view_group_permission) == (True, None)
    assert can_grant_direct_permission(
        actor,
        Permission.objects.get(content_type__app_label="auth", codename="change_permission"),
    ) == (False, "permission_non_delegable")
