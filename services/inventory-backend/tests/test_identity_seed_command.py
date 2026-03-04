from io import StringIO

import pytest
from django.core.management import call_command

from apps.identity.models import EthnicityCode, GenderCode, PrefixCode, RaceCode, SuffixCode


@pytest.mark.django_db
def test_seed_identity_code_tables_creates_expected_rows() -> None:
    out = StringIO()

    call_command("seed_identity_code_tables", stdout=out)

    assert PrefixCode.objects.filter(code="mr", label="Mr.").exists()
    assert SuffixCode.objects.filter(code="phd", label="Ph.D.").exists()
    assert GenderCode.objects.filter(code="nonbinary", label="Nonbinary").exists()
    assert RaceCode.objects.filter(
        code="american_indian",
        label="American Indian or Alaska Native",
    ).exists()
    assert EthnicityCode.objects.filter(
        code="hispanic_latino",
        label="Hispanic or Latino",
    ).exists()


@pytest.mark.django_db
def test_seed_identity_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    PrefixCode.objects.create(
        code="mr",
        label="Mister",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_identity_code_tables")
    call_command("seed_identity_code_tables")

    mr = PrefixCode.objects.get(code="mr")

    assert PrefixCode.objects.count() == 6
    assert SuffixCode.objects.count() == 7
    assert GenderCode.objects.count() == 6
    assert RaceCode.objects.count() == 7
    assert EthnicityCode.objects.count() == 4
    assert mr.label == "Mr."
    assert mr.sort_order == 10
    assert mr.is_system_managed is True
    assert mr.is_active is True


@pytest.mark.django_db
def test_seed_identity_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_identity_code_tables", dry_run=True)

    assert PrefixCode.objects.count() == 0
    assert SuffixCode.objects.count() == 0
