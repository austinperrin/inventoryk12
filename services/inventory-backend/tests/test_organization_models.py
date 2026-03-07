from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError

from apps.identity.models import RoleAssignment, RoleAssignmentOrganization
from apps.locations.models import Address, AddressCode
from apps.organization.models import (
    Organization,
    OrganizationAdditionalIdentifier,
    OrganizationAddress,
    OrganizationCode,
    OrganizationLifecycle,
)

User = get_user_model()


def _user(**overrides):
    data = {
        "email": "person@example.com",
        "password": "ChangeMe123!",
    }
    data.update(overrides)
    return User.objects.create_user(**data)


def _organization_type(**overrides):
    data = {
        "local_id": "district",
        "code": "district",
        "label": "District",
        "sort_order": 10,
    }
    data.update(overrides)
    return OrganizationCode.objects.create(**data)


def _organization(**overrides):
    organization_code = overrides.pop("organization_code", None) or _organization_type()
    data = {
        "local_id": "demoisd",
        "name": "Demo ISD",
        "organization_code": organization_code,
    }
    data.update(overrides)
    return Organization.objects.create(**data)


def _address(**overrides):
    data = {
        "line_1": "123 Main St",
        "city": "Austin",
    }
    data.update(overrides)
    return Address.objects.create(**data)


def _address_code(**overrides):
    data = {
        "code": "physical",
        "label": "Physical",
        "sort_order": 10,
    }
    data.update(overrides)
    return AddressCode.objects.create(**data)


@pytest.mark.django_db
def test_organization_string_uses_display_name_when_present() -> None:
    organization = _organization(display_name="Demo Independent School District")

    assert str(organization) == "Demo Independent School District"


@pytest.mark.django_db(transaction=True)
def test_organization_lifecycle_rejects_invalid_date_window() -> None:
    organization = _organization()

    with pytest.raises(IntegrityError):
        OrganizationLifecycle.objects.create(
            organization=organization,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_organization_address_rejects_invalid_date_window() -> None:
    organization = _organization()
    address = _address()
    address_code = _address_code()

    with pytest.raises(IntegrityError):
        OrganizationAddress.objects.create(
            organization=organization,
            address=address,
            address_code=address_code,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_organization_address_is_unique_per_org_address_and_type() -> None:
    organization = _organization()
    address = _address()
    address_code = _address_code()
    OrganizationAddress.objects.create(
        organization=organization,
        address=address,
        address_code=address_code,
    )

    with pytest.raises(IntegrityError):
        OrganizationAddress.objects.create(
            organization=organization,
            address=address,
            address_code=address_code,
        )


@pytest.mark.django_db(transaction=True)
def test_organization_additional_identifier_rejects_invalid_date_window() -> None:
    organization = _organization()

    with pytest.raises(IntegrityError):
        OrganizationAdditionalIdentifier.objects.create(
            organization=organization,
            system="sis",
            identifier_type="district_id",
            identifier_value="001",
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_organization_additional_identifier_is_unique_per_scope() -> None:
    organization = _organization()
    OrganizationAdditionalIdentifier.objects.create(
        organization=organization,
        system="sis",
        identifier_type="district_id",
        identifier_value="001",
    )

    with pytest.raises(IntegrityError):
        OrganizationAdditionalIdentifier.objects.create(
            organization=organization,
            system="sis",
            identifier_type="district_id",
            identifier_value="001",
        )


@pytest.mark.django_db(transaction=True)
def test_role_assignment_organization_is_unique_per_assignment_and_org() -> None:
    user = _user(email="teacher@example.com")
    role = Group.objects.create(name="teacher")
    assignment = RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=date(2026, 4, 1),
    )
    organization = _organization()

    RoleAssignmentOrganization.objects.create(
        role_assignment=assignment,
        organization=organization,
    )

    with pytest.raises(IntegrityError):
        RoleAssignmentOrganization.objects.create(
            role_assignment=assignment,
            organization=organization,
        )
