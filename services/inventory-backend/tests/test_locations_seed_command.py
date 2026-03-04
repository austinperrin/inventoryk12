from io import StringIO

import pytest
from django.core.management import call_command

from apps.locations.models import CountryCode, FacilityCode, StateCode


@pytest.mark.django_db
def test_seed_locations_code_tables_creates_expected_rows() -> None:
    out = StringIO()

    call_command("seed_locations_code_tables", stdout=out)

    assert CountryCode.objects.filter(code="US", label="United States").exists()
    assert StateCode.objects.filter(code="TX", label="Texas").exists()
    assert StateCode.objects.filter(code="CA", label="California").exists()
    assert FacilityCode.objects.filter(code="campus", label="Campus").exists()
    assert FacilityCode.objects.filter(code="warehouse", label="Warehouse").exists()


@pytest.mark.django_db
def test_seed_locations_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    StateCode.objects.create(
        code="TX",
        label="Tex.",
        description="Old value",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_locations_code_tables")
    call_command("seed_locations_code_tables")

    texas = StateCode.objects.get(code="TX")

    assert CountryCode.objects.count() == 1
    assert StateCode.objects.count() == 51
    assert FacilityCode.objects.count() == 5
    assert texas.label == "Texas"
    assert texas.description == ""
    assert texas.sort_order == 440
    assert texas.is_system_managed is True
    assert texas.is_active is True


@pytest.mark.django_db
def test_seed_locations_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_locations_code_tables", dry_run=True)

    assert CountryCode.objects.count() == 0
    assert StateCode.objects.count() == 0
    assert FacilityCode.objects.count() == 0
