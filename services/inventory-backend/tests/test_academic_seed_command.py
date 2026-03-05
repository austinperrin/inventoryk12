from io import StringIO

import pytest
from django.core.management import call_command

from apps.academic.models import AcademicTermCode


@pytest.mark.django_db
def test_seed_academic_code_tables_creates_expected_rows() -> None:
    out = StringIO()

    call_command("seed_academic_code_tables", stdout=out)

    assert AcademicTermCode.objects.filter(code="year", label="Year").exists()
    assert AcademicTermCode.objects.filter(code="semester", label="Semester").exists()
    assert AcademicTermCode.objects.filter(code="quarter", label="Quarter").exists()


@pytest.mark.django_db
def test_seed_academic_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    AcademicTermCode.objects.create(
        code="semester",
        label="Sem",
        description="Old value",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_academic_code_tables")
    call_command("seed_academic_code_tables")

    semester = AcademicTermCode.objects.get(code="semester")

    assert AcademicTermCode.objects.count() == 4
    assert semester.label == "Semester"
    assert semester.description == ""
    assert semester.sort_order == 20
    assert semester.is_system_managed is True
    assert semester.is_active is True


@pytest.mark.django_db
def test_seed_academic_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_academic_code_tables", dry_run=True)

    assert AcademicTermCode.objects.count() == 0
