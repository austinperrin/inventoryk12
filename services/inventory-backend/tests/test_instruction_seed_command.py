import io

import pytest
from django.core.management import call_command

from apps.instruction.models import GradeLevelCode, SubjectCode


@pytest.mark.django_db
def test_seed_instruction_code_tables_creates_expected_rows() -> None:
    out = io.StringIO()

    call_command("seed_instruction_code_tables", stdout=out)
    output = out.getvalue()

    assert "SubjectCode: created=" in output
    assert "GradeLevelCode: created=" in output
    assert SubjectCode.objects.filter(code="math").exists()
    assert GradeLevelCode.objects.filter(code="kg").exists()


@pytest.mark.django_db
def test_seed_instruction_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    SubjectCode.objects.create(
        code="math",
        label="Old Math Label",
        description="Old Description",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_instruction_code_tables")
    call_command("seed_instruction_code_tables")

    math = SubjectCode.objects.get(code="math")
    assert math.label == "Mathematics"
    assert math.sort_order == 10
    assert math.is_system_managed is True
    assert math.is_active is True
    assert SubjectCode.objects.filter(code="math").count() == 1


@pytest.mark.django_db
def test_seed_instruction_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_instruction_code_tables", dry_run=True)

    assert SubjectCode.objects.count() == 0
    assert GradeLevelCode.objects.count() == 0
