from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.contacts.models import (
    Email,
    EmailCode,
    Phone,
    PhoneCode,
    StaffAssignment,
    StudentGuardianRelationship,
    StudentRelationship,
    UserAddress,
)
from apps.locations.models import Address, AddressCode, CountryCode, Facility, FacilityCode, StateCode
from apps.organization.models import Organization, OrganizationCode

User = get_user_model()


def _user(**overrides):
    data = {
        "email": "person@example.com",
        "password": "ChangeMe123!",
    }
    data.update(overrides)
    return User.objects.create_user(**data)


def _phone_code(**overrides):
    data = {
        "code": "mobile",
        "label": "Mobile",
        "sort_order": 10,
    }
    data.update(overrides)
    return PhoneCode.objects.create(**data)


def _email_code(**overrides):
    data = {
        "code": "personal",
        "label": "Personal",
        "sort_order": 10,
    }
    data.update(overrides)
    return EmailCode.objects.create(**data)


def _country(**overrides):
    data = {
        "code": "US",
        "label": "United States",
        "sort_order": 10,
    }
    data.update(overrides)
    return CountryCode.objects.create(**data)


def _state(**overrides):
    data = {
        "code": "TX",
        "label": "Texas",
        "sort_order": 10,
    }
    data.update(overrides)
    return StateCode.objects.create(**data)


def _address(**overrides):
    country_code = overrides.pop("country_code", None) or _country()
    state_code = overrides.pop("state_code", None) or _state()
    data = {
        "line_1": "123 Main St",
        "city": "Austin",
        "state_code": state_code,
        "postal_code": "78701",
        "country_code": country_code,
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


def _organization_code(**overrides):
    data = {
        "local_id": "district",
        "code": "district",
        "label": "District",
        "sort_order": 10,
    }
    data.update(overrides)
    return OrganizationCode.objects.create(**data)


def _organization(**overrides):
    organization_code = overrides.pop("organization_code", None) or _organization_code()
    data = {
        "local_id": "demoisd",
        "name": "Demo ISD",
        "organization_code": organization_code,
    }
    data.update(overrides)
    return Organization.objects.create(**data)


def _facility_code(**overrides):
    data = {
        "code": "campus",
        "label": "Campus",
        "sort_order": 10,
    }
    data.update(overrides)
    return FacilityCode.objects.create(**data)


def _facility(**overrides):
    facility_code = overrides.pop("facility_code", None) or _facility_code()
    data = {
        "local_id": "campus-001",
        "name": "Demo Campus",
        "facility_code": facility_code,
    }
    data.update(overrides)
    return Facility.objects.create(**data)


@pytest.mark.django_db(transaction=True)
def test_phone_enforces_single_primary_per_user() -> None:
    user = _user()
    phone_code = _phone_code()
    Phone.objects.create(
        user=user,
        phone_number="5125551000",
        phone_code=phone_code,
        is_primary=True,
    )

    with pytest.raises(IntegrityError):
        Phone.objects.create(
            user=user,
            phone_number="5125552000",
            phone_code=phone_code,
            is_primary=True,
        )


@pytest.mark.django_db(transaction=True)
def test_email_enforces_single_primary_per_user() -> None:
    user = _user()
    email_code = _email_code()
    Email.objects.create(
        user=user,
        email_address="first@example.com",
        email_code=email_code,
        is_primary=True,
    )

    with pytest.raises(IntegrityError):
        Email.objects.create(
            user=user,
            email_address="second@example.com",
            email_code=email_code,
            is_primary=True,
        )


@pytest.mark.django_db(transaction=True)
def test_user_address_rejects_invalid_date_window() -> None:
    user = _user()
    address = _address()
    address_code = _address_code()

    with pytest.raises(IntegrityError):
        UserAddress.objects.create(
            user=user,
            address=address,
            address_code=address_code,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_user_address_allows_only_one_primary_per_type() -> None:
    user = _user()
    country = _country()
    state = _state()
    first_address = _address(country_code=country, state_code=state)
    second_address = _address(
        line_1="456 Oak Ave",
        postal_code="78702",
        country_code=country,
        state_code=state,
    )
    address_code = _address_code()
    UserAddress.objects.create(
        user=user,
        address=first_address,
        address_code=address_code,
        is_primary=True,
    )

    with pytest.raises(IntegrityError):
        UserAddress.objects.create(
            user=user,
            address=second_address,
            address_code=address_code,
            is_primary=True,
        )


@pytest.mark.django_db(transaction=True)
def test_student_relationship_rejects_self_relationship() -> None:
    student = _user(email="student@example.com")

    with pytest.raises(IntegrityError):
        StudentRelationship.objects.create(
            student=student,
            related_student=student,
        )


@pytest.mark.django_db(transaction=True)
def test_student_guardian_relationship_allows_only_one_primary_contact() -> None:
    student = _user(email="student@example.com")
    first_guardian = _user(email="guardian1@example.com")
    second_guardian = _user(email="guardian2@example.com")
    StudentGuardianRelationship.objects.create(
        student=student,
        guardian=first_guardian,
        is_primary_contact=True,
    )

    with pytest.raises(IntegrityError):
        StudentGuardianRelationship.objects.create(
            student=student,
            guardian=second_guardian,
            is_primary_contact=True,
        )


@pytest.mark.django_db(transaction=True)
def test_staff_assignment_requires_exactly_one_scope() -> None:
    staff = _user(email="staff@example.com")
    organization = _organization()
    facility = _facility()

    with pytest.raises(IntegrityError):
        StaffAssignment.objects.create(
            staff=staff,
            organization=organization,
            facility=facility,
            starts_on=date(2026, 4, 1),
        )

    with pytest.raises(IntegrityError):
        StaffAssignment.objects.create(
            staff=staff,
            starts_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_staff_assignment_rejects_invalid_date_window() -> None:
    staff = _user(email="staff@example.com")
    organization = _organization()

    with pytest.raises(IntegrityError):
        StaffAssignment.objects.create(
            staff=staff,
            organization=organization,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )
