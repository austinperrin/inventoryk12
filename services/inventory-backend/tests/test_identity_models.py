from datetime import date, timedelta

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError
from django.utils import timezone

from apps.identity.models import (
    Profile,
    RoleAssignment,
    StudentDetail,
    UserAdditionalIdentifier,
    UserLoginLock,
)
from apps.locations.models import CountryCode, StateCode

User = get_user_model()


def _user(**overrides):
    data = {
        "email": "person@example.com",
        "password": "ChangeMe123!",
    }
    data.update(overrides)
    return User.objects.create_user(**data)


@pytest.mark.django_db
def test_profile_can_be_created_without_slug() -> None:
    user = _user()

    profile = Profile.objects.create(user=user, preferred_name="Ada")

    assert profile.slug is None
    assert str(profile) == "Ada"


@pytest.mark.django_db(transaction=True)
def test_profile_slug_must_be_unique_when_present() -> None:
    first_user = _user(email="first@example.com")
    second_user = _user(email="second@example.com")

    Profile.objects.create(user=first_user, slug="ada-lovelace")

    with pytest.raises(IntegrityError):
        Profile.objects.create(user=second_user, slug="ada-lovelace")


@pytest.mark.django_db
def test_role_assignment_is_active_on_window_boundaries() -> None:
    user = _user()
    role = Group.objects.create(name="teacher")
    assignment = RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=date(2026, 3, 1),
        ends_on=date(2026, 3, 31),
    )

    assert assignment.is_active_on(date(2026, 3, 1)) is True
    assert assignment.is_active_on(date(2026, 3, 15)) is True
    assert assignment.is_active_on(date(2026, 3, 31)) is True
    assert assignment.is_active_on(date(2026, 4, 1)) is False


@pytest.mark.django_db(transaction=True)
def test_role_assignment_rejects_invalid_date_window() -> None:
    user = _user()
    role = Group.objects.create(name="principal")

    with pytest.raises(IntegrityError):
        RoleAssignment.objects.create(
            user=user,
            role=role,
            starts_on=date(2026, 3, 10),
            ends_on=date(2026, 3, 9),
        )


@pytest.mark.django_db(transaction=True)
def test_user_login_lock_rejects_invalid_window() -> None:
    user = _user()
    starts_at = timezone.now()

    with pytest.raises(IntegrityError):
        UserLoginLock.objects.create(
            user=user,
            starts_at=starts_at,
            ends_at=starts_at - timedelta(minutes=1),
        )


@pytest.mark.django_db(transaction=True)
def test_user_additional_identifier_is_unique_per_user_and_source() -> None:
    user = _user()
    UserAdditionalIdentifier.objects.create(
        user=user,
        system="sis",
        identifier_type="student_number",
        identifier_value="12345",
    )

    with pytest.raises(IntegrityError):
        UserAdditionalIdentifier.objects.create(
            user=user,
            system="sis",
            identifier_type="student_number",
            identifier_value="12345",
        )


@pytest.mark.django_db
def test_student_detail_uses_locations_birth_foreign_keys() -> None:
    user = _user(email="student@example.com")
    country = CountryCode.objects.create(code="US", label="United States")
    state = StateCode.objects.create(code="TX", label="Texas")

    detail = StudentDetail.objects.create(
        user=user,
        birth_country=country,
        birth_state=state,
        birth_city="Austin",
    )

    assert detail.birth_country == country
    assert detail.birth_state == state
    assert detail.birth_city == "Austin"


@pytest.mark.django_db
def test_auth_group_and_permission_history_are_registered() -> None:
    historical_group_model = apps.get_model("identity", "HistoricalGroup")
    historical_group_permissions_model = apps.get_model("identity", "HistoricalGroup_permissions")
    historical_permission_model = apps.get_model("identity", "HistoricalPermission")

    permission = Permission.objects.first()
    assert permission is not None

    group = Group.objects.create(name="campus_scheduler")
    group.permissions.add(permission)
    permission.name = f"{permission.name} (history)"
    permission.save(update_fields=["name"])

    assert historical_group_model.objects.filter(id=group.id).exists()
    assert historical_group_permissions_model.objects.filter(group_id=group.id).exists()
    assert historical_permission_model.objects.filter(id=permission.id).exists()
