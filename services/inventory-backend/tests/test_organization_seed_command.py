from io import StringIO

import pytest
from django.core.management import call_command

from apps.organization.models import OrganizationTypeCode


@pytest.mark.django_db
def test_seed_organization_code_tables_creates_expected_rows() -> None:
    out = StringIO()

    call_command("seed_organization_code_tables", stdout=out)

    assert OrganizationTypeCode.objects.filter(
        local_id="district",
        code="district",
        label="District",
    ).exists()
    assert OrganizationTypeCode.objects.filter(
        local_id="school",
        code="school",
        label="School",
    ).exists()
    assert OrganizationTypeCode.objects.filter(
        local_id="department",
        code="department",
        label="Department",
    ).exists()


@pytest.mark.django_db
def test_seed_organization_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    OrganizationTypeCode.objects.create(
        local_id="district",
        code="lea",
        label="Local Education Agency",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_organization_code_tables")
    call_command("seed_organization_code_tables")

    district = OrganizationTypeCode.objects.get(local_id="district")

    assert OrganizationTypeCode.objects.count() == 3
    assert district.code == "district"
    assert district.label == "District"
    assert district.sort_order == 10
    assert district.is_system_managed is True
    assert district.is_active is True


@pytest.mark.django_db
def test_seed_organization_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_organization_code_tables", dry_run=True)

    assert OrganizationTypeCode.objects.count() == 0
