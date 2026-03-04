from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.identity.models import StudentDetail
from apps.locations.models import (
    Address,
    AddressValidationRun,
    CountryCode,
    Facility,
    FacilityAdditionalIdentifier,
    FacilityAddress,
    FacilityLifecycle,
    FacilityTypeCode,
    OrganizationFacility,
    StateCode,
)
from apps.organization.models import Organization, OrganizationAddress, OrganizationCode

User = get_user_model()


def _user(**overrides):
    data = {
        "email": "person@example.com",
        "password": "ChangeMe123!",
    }
    data.update(overrides)
    return User.objects.create_user(**data)


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


def _facility_type(**overrides):
    data = {
        "code": "campus",
        "label": "Campus",
        "sort_order": 10,
    }
    data.update(overrides)
    return FacilityTypeCode.objects.create(**data)


def _facility(**overrides):
    facility_type_code = overrides.pop("facility_type_code", None) or _facility_type()
    data = {
        "local_id": "campus-001",
        "name": "Demo Campus",
        "facility_type_code": facility_type_code,
    }
    data.update(overrides)
    return Facility.objects.create(**data)


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


@pytest.mark.django_db(transaction=True)
def test_facility_lifecycle_rejects_invalid_date_window() -> None:
    facility = _facility()

    with pytest.raises(IntegrityError):
        FacilityLifecycle.objects.create(
            facility=facility,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_facility_address_is_unique_per_facility_address_and_type() -> None:
    facility = _facility()
    address = _address()
    FacilityAddress.objects.create(
        facility=facility,
        address=address,
        address_type=FacilityAddress.AddressType.PHYSICAL,
    )

    with pytest.raises(IntegrityError):
        FacilityAddress.objects.create(
            facility=facility,
            address=address,
            address_type=FacilityAddress.AddressType.PHYSICAL,
        )


@pytest.mark.django_db(transaction=True)
def test_organization_facility_rejects_invalid_date_window() -> None:
    organization = _organization()
    facility = _facility()

    with pytest.raises(IntegrityError):
        OrganizationFacility.objects.create(
            organization=organization,
            facility=facility,
            starts_on=date(2026, 4, 2),
            ends_on=date(2026, 4, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_facility_additional_identifier_is_unique_per_scope() -> None:
    facility = _facility()
    FacilityAdditionalIdentifier.objects.create(
        facility=facility,
        system="sis",
        identifier_type="facility_id",
        identifier_value="A100",
    )

    with pytest.raises(IntegrityError):
        FacilityAdditionalIdentifier.objects.create(
            facility=facility,
            system="sis",
            identifier_type="facility_id",
            identifier_value="A100",
        )


@pytest.mark.django_db
def test_identity_birth_location_fields_use_locations_foreign_keys() -> None:
    user = _user(email="student@example.com")
    country = _country()
    state = _state()

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
def test_organization_address_uses_locations_address_foreign_key() -> None:
    organization = _organization()
    address = _address()

    link = OrganizationAddress.objects.create(
        organization=organization,
        address=address,
        address_type=OrganizationAddress.AddressType.PHYSICAL,
    )

    assert link.address == address


@pytest.mark.django_db
def test_address_validation_run_defaults_to_internal_provider() -> None:
    address = _address()

    run = AddressValidationRun.objects.create(address=address)

    assert run.provider_requested == "internal"
