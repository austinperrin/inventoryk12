import io

import pytest
from django.core.management import call_command

from apps.enrollment.models import EnrollmentEntryCode, EnrollmentExitCode, StaffAssignmentRoleCode
from apps.enrollment.seeds import (
    ENROLLMENT_ENTRY_CODE_SEEDS,
    ENROLLMENT_EXIT_CODE_SEEDS,
    STAFF_ASSIGNMENT_ROLE_CODE_SEEDS,
)


@pytest.mark.django_db
def test_seed_enrollment_code_tables_creates_expected_rows() -> None:
    out = io.StringIO()
    call_command("seed_enrollment_code_tables", stdout=out)
    output = out.getvalue()

    assert "EnrollmentEntryCode: created=" in output
    assert "EnrollmentExitCode: created=" in output
    assert "StaffAssignmentRoleCode: created=" in output
    assert EnrollmentEntryCode.objects.count() == len(ENROLLMENT_ENTRY_CODE_SEEDS)
    assert EnrollmentExitCode.objects.count() == len(ENROLLMENT_EXIT_CODE_SEEDS)
    assert StaffAssignmentRoleCode.objects.count() == len(STAFF_ASSIGNMENT_ROLE_CODE_SEEDS)


@pytest.mark.django_db
def test_seed_enrollment_code_tables_is_idempotent_and_updates_existing_rows() -> None:
    EnrollmentEntryCode.objects.create(
        code="new_enrollment",
        label="Old Label",
        description="Old Description",
        sort_order=999,
        is_system_managed=False,
        is_active=False,
    )

    call_command("seed_enrollment_code_tables")
    call_command("seed_enrollment_code_tables")

    entry = EnrollmentEntryCode.objects.get(code="new_enrollment")
    assert entry.label == "New Enrollment"
    assert entry.description == "Student is newly enrolled in the organization or section."
    assert entry.sort_order == 10
    assert entry.is_system_managed is True
    assert entry.is_active is True
    assert EnrollmentEntryCode.objects.filter(code="new_enrollment").count() == 1


@pytest.mark.django_db
def test_seed_enrollment_code_tables_dry_run_does_not_persist_rows() -> None:
    call_command("seed_enrollment_code_tables", dry_run=True)

    assert EnrollmentEntryCode.objects.count() == 0
    assert EnrollmentExitCode.objects.count() == 0
    assert StaffAssignmentRoleCode.objects.count() == 0
