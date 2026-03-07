from datetime import date
from itertools import count

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from apps.academic.models import AcademicTerm, AcademicTermCode, AcademicYear
from apps.enrollment.models import (
    EnrollmentEntryCode,
    EnrollmentExitCode,
    StaffAssignmentRoleCode,
    StaffSchedule,
    StudentEnrollment,
    StudentSchedule,
)
from apps.identity.models import RoleAssignment, RoleAssignmentOrganization
from apps.instruction.models import Course, GradeLevelCode, Section, SubjectCode
from apps.organization.models import Organization, OrganizationCode

User = get_user_model()
_SEQ = count(1)


def _user(**overrides):
    data = {
        "email": f"user{next(_SEQ)}@example.com",
        "password": "ChangeMe123!",
    }
    data.update(overrides)
    return User.objects.create_user(**data)


def _organization_code(**overrides):
    n = next(_SEQ)
    data = {
        "local_id": f"school-{n}",
        "code": f"school_{n}",
        "label": f"School {n}",
        "sort_order": 10,
    }
    data.update(overrides)
    return OrganizationCode.objects.create(**data)


def _organization(**overrides):
    n = next(_SEQ)
    organization_code = overrides.pop("organization_code", None) or _organization_code()
    data = {
        "local_id": f"demo-high-{n}",
        "name": f"Demo High School {n}",
        "organization_code": organization_code,
    }
    data.update(overrides)
    return Organization.objects.create(**data)


def _academic_year(**overrides):
    organization = overrides.pop("organization", None) or _organization()
    data = {
        "year_code": 2026,
        "label": "2025-2026",
        "organization": organization,
        "starts_on": date(2025, 8, 1),
        "ends_on": date(2026, 5, 31),
    }
    data.update(overrides)
    return AcademicYear.objects.create(**data)


def _term_code(**overrides):
    n = next(_SEQ)
    data = {
        "code": f"semester_{n}",
        "label": f"Semester {n}",
        "sort_order": 10,
    }
    data.update(overrides)
    return AcademicTermCode.objects.create(**data)


def _academic_term(**overrides):
    academic_year = overrides.pop("academic_year", None) or _academic_year()
    term_code = overrides.pop("term_code", None) or _term_code()
    data = {
        "academic_year": academic_year,
        "organization": academic_year.organization,
        "term_code": term_code,
        "code": f"FALL-{next(_SEQ)}",
        "label": "Fall",
        "starts_on": date(2025, 8, 1),
        "ends_on": date(2025, 12, 20),
    }
    data.update(overrides)
    return AcademicTerm.objects.create(**data)


def _subject_code(**overrides):
    n = next(_SEQ)
    data = {
        "code": f"science_{n}",
        "label": "Science",
        "sort_order": 10,
    }
    data.update(overrides)
    return SubjectCode.objects.create(**data)


def _grade_level_code(**overrides):
    data = {
        "code": f"08_{next(_SEQ)}",
        "label": "Grade 8",
        "sort_order": 80,
    }
    data.update(overrides)
    return GradeLevelCode.objects.create(**data)


def _course(**overrides):
    organization = overrides.pop("organization", None) or _organization()
    subject_code = overrides.pop("subject_code", None) or _subject_code()
    grade_low_code = overrides.pop("grade_low_code", None) or _grade_level_code(label="Grade 6")
    grade_high_code = overrides.pop("grade_high_code", None) or _grade_level_code(label="Grade 8")
    data = {
        "organization": organization,
        "course_code": f"SCI-8-{next(_SEQ)}",
        "title": "Science 8",
        "subject_code": subject_code,
        "grade_low_code": grade_low_code,
        "grade_high_code": grade_high_code,
    }
    data.update(overrides)
    return Course.objects.create(**data)


def _section(**overrides):
    course = overrides.pop("course", None) or _course()
    data = {
        "course": course,
        "organization": course.organization,
        "academic_term": _academic_term(organization=course.organization),
        "section_code": f"A-{next(_SEQ)}",
        "starts_on": date(2025, 8, 15),
        "ends_on": date(2025, 12, 18),
    }
    data.update(overrides)
    return Section.objects.create(**data)


def _entry_code(**overrides):
    data = {
        "code": f"entry_{next(_SEQ)}",
        "label": "Entry",
        "sort_order": 10,
    }
    data.update(overrides)
    return EnrollmentEntryCode.objects.create(**data)


def _exit_code(**overrides):
    data = {
        "code": f"exit_{next(_SEQ)}",
        "label": "Exit",
        "sort_order": 10,
    }
    data.update(overrides)
    return EnrollmentExitCode.objects.create(**data)


def _staff_role_code(**overrides):
    data = {
        "code": f"role_{next(_SEQ)}",
        "label": "Teacher of Record",
        "sort_order": 10,
    }
    data.update(overrides)
    return StaffAssignmentRoleCode.objects.create(**data)


@pytest.mark.django_db
def test_student_enrollment_rejects_overlapping_windows() -> None:
    student = _user()
    organization = _organization()
    grade_level = _grade_level_code(code=f"08_{next(_SEQ)}")
    StudentEnrollment.objects.create(
        student_user=student,
        organization=organization,
        grade_level_code=grade_level,
        starts_on=date(2025, 8, 1),
        ends_on=date(2025, 12, 1),
    )

    with pytest.raises(ValidationError):
        StudentEnrollment.objects.create(
            student_user=student,
            organization=organization,
            grade_level_code=grade_level,
            starts_on=date(2025, 10, 1),
            ends_on=date(2026, 1, 1),
        )


@pytest.mark.django_db
def test_student_enrollment_role_assignment_links_must_match_student_and_org() -> None:
    organization = _organization()
    role = Group.objects.create(name=f"student_{next(_SEQ)}")
    student = _user()
    other_user = _user()
    assignment = RoleAssignment.objects.create(
        user=other_user,
        role=role,
        starts_on=date(2025, 8, 1),
    )
    assignment_org = RoleAssignmentOrganization.objects.create(
        role_assignment=assignment,
        organization=organization,
    )

    with pytest.raises(ValidationError):
        StudentEnrollment.objects.create(
            student_user=student,
            organization=organization,
            grade_level_code=_grade_level_code(code=f"09_{next(_SEQ)}"),
            starts_on=date(2025, 8, 1),
            role_assignment=assignment,
            role_assignment_org=assignment_org,
        )


@pytest.mark.django_db
def test_student_schedule_enforces_section_windows_and_overlap() -> None:
    section = _section()
    student = _user()
    StudentSchedule.objects.create(
        section=section,
        student_user=student,
        starts_on=date(2025, 8, 15),
        ends_on=date(2025, 12, 18),
        entry_code=_entry_code(),
        exit_code=_exit_code(),
    )

    with pytest.raises(ValidationError):
        StudentSchedule.objects.create(
            section=section,
            student_user=student,
            starts_on=date(2025, 9, 1),
            ends_on=date(2025, 10, 1),
        )

    with pytest.raises(ValidationError):
        StudentSchedule.objects.create(
            section=section,
            student_user=student,
            starts_on=date(2025, 8, 1),
        )

    with pytest.raises(ValidationError):
        StudentSchedule.objects.create(
            section=section,
            student_user=student,
            starts_on=date(2025, 9, 1),
            ends_on=date(2025, 12, 20),
        )


@pytest.mark.django_db
def test_staff_schedule_enforces_section_windows_and_overlap() -> None:
    section = _section()
    staff_user = _user()
    StaffSchedule.objects.create(
        section=section,
        staff_user=staff_user,
        starts_on=date(2025, 8, 15),
        ends_on=date(2025, 12, 18),
        staff_assignment_role_code=_staff_role_code(),
        is_primary=True,
    )

    with pytest.raises(ValidationError):
        StaffSchedule.objects.create(
            section=section,
            staff_user=staff_user,
            starts_on=date(2025, 9, 1),
            ends_on=date(2025, 10, 1),
        )

    with pytest.raises(ValidationError):
        StaffSchedule.objects.create(
            section=section,
            staff_user=staff_user,
            starts_on=date(2025, 8, 1),
        )
