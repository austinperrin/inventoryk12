from io import StringIO

import pytest
from django.core.management import call_command

from apps.contacts.models import EmailCode, PhoneCode


@pytest.mark.django_db
def test_seed_contacts_code_tables_creates_expected_rows() -> None:
    out = StringIO()

    call_command("seed_contacts_code_tables", stdout=out)

    assert PhoneCode.objects.filter(code="mobile", label="Mobile").exists()
    assert PhoneCode.objects.filter(code="work", label="Work").exists()
    assert EmailCode.objects.filter(code="personal", label="Personal").exists()
    assert EmailCode.objects.filter(code="notification", label="Notification").exists()


@pytest.mark.django_db
def test_seed_contacts_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    PhoneCode.objects.create(
        code="mobile",
        label="Cell",
        description="Old value",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_contacts_code_tables")
    call_command("seed_contacts_code_tables")

    mobile = PhoneCode.objects.get(code="mobile")

    assert PhoneCode.objects.count() == 4
    assert EmailCode.objects.count() == 3
    assert mobile.label == "Mobile"
    assert mobile.description == ""
    assert mobile.sort_order == 10
    assert mobile.is_system_managed is True
    assert mobile.is_active is True


@pytest.mark.django_db
def test_seed_contacts_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_contacts_code_tables", dry_run=True)

    assert PhoneCode.objects.count() == 0
    assert EmailCode.objects.count() == 0
