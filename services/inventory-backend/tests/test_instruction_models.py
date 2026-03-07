from datetime import date, time
from itertools import count

import pytest
from django.db import IntegrityError

from apps.academic.models import AcademicTerm, AcademicTermCode, AcademicYear
from apps.instruction.models import (
    Course,
    CourseAdditionalIdentifier,
    GradeLevelCode,
    Period,
    Section,
    SectionAdditionalIdentifier,
    SectionMeetingPattern,
    SubjectCode,
)
from apps.locations.models import Facility, FacilityCode
from apps.organization.models import Organization, OrganizationCode

_SEQ = count(1)


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
        "code": "08",
        "label": "Grade 8",
        "sort_order": 80,
    }
    data.update(overrides)
    return GradeLevelCode.objects.create(**data)


def _course(**overrides):
    organization = overrides.pop("organization", None) or _organization()
    subject_code = overrides.pop("subject_code", None) or _subject_code()
    grade_low_code = overrides.pop("grade_low_code", None) or _grade_level_code(
        code="06", label="Grade 6"
    )
    grade_high_code = overrides.pop("grade_high_code", None) or _grade_level_code(
        code="08", label="Grade 8"
    )
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
    organization = overrides.pop("organization", None)
    course = overrides.pop("course", None)
    if course is None:
        course = _course(organization=organization) if organization else _course()
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


def _facility_code(**overrides):
    n = next(_SEQ)
    data = {
        "code": f"room_{n}",
        "label": "Room",
        "sort_order": 10,
    }
    data.update(overrides)
    return FacilityCode.objects.create(**data)


def _facility(**overrides):
    n = next(_SEQ)
    facility_code = overrides.pop("facility_code", None) or _facility_code()
    data = {
        "local_id": f"room-{n}",
        "name": f"Room {n}",
        "facility_code": facility_code,
    }
    data.update(overrides)
    return Facility.objects.create(**data)


@pytest.mark.django_db(transaction=True)
def test_course_is_unique_per_org_and_code() -> None:
    organization = _organization()
    subject_code = _subject_code()
    grade_low_code = _grade_level_code(code="09", label="Grade 9", sort_order=90)
    grade_high_code = _grade_level_code(code="10", label="Grade 10", sort_order=100)
    Course.objects.create(
        organization=organization,
        course_code="ALG-1",
        title="Algebra 1",
        subject_code=subject_code,
        grade_low_code=grade_low_code,
        grade_high_code=grade_high_code,
    )

    with pytest.raises(IntegrityError):
        Course.objects.create(
            organization=organization,
            course_code="ALG-1",
            title="Algebra 1 Duplicate",
            subject_code=subject_code,
        )


@pytest.mark.django_db(transaction=True)
def test_section_requires_valid_window_and_unique_scope() -> None:
    section = _section()

    with pytest.raises(IntegrityError):
        Section.objects.create(
            course=section.course,
            organization=section.organization,
            academic_term=section.academic_term,
            section_code=section.section_code,
        )

    with pytest.raises(IntegrityError):
        Section.objects.create(
            course=section.course,
            organization=section.organization,
            academic_term=section.academic_term,
            section_code="A-102",
            starts_on=date(2025, 12, 20),
            ends_on=date(2025, 8, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_additional_identifier_models_enforce_uniqueness_and_windows() -> None:
    course = _course()
    section = _section(course=course)
    CourseAdditionalIdentifier.objects.create(
        course=course,
        system="sis",
        identifier_type="course_id",
        identifier_value="C-100",
    )
    SectionAdditionalIdentifier.objects.create(
        section=section,
        system="sis",
        identifier_type="section_id",
        identifier_value="S-100",
    )

    with pytest.raises(IntegrityError):
        CourseAdditionalIdentifier.objects.create(
            course=course,
            system="sis",
            identifier_type="course_id",
            identifier_value="C-100",
        )

    with pytest.raises(IntegrityError):
        SectionAdditionalIdentifier.objects.create(
            section=section,
            system="sis",
            identifier_type="section_id",
            identifier_value="S-100",
        )

    with pytest.raises(IntegrityError):
        SectionAdditionalIdentifier.objects.create(
            section=section,
            system="sis",
            identifier_type="section_id",
            identifier_value="S-101",
            starts_on=date(2025, 9, 2),
            ends_on=date(2025, 9, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_period_and_meeting_pattern_enforce_time_and_date_windows() -> None:
    organization = _organization()
    period = Period.objects.create(
        organization=organization,
        period_code="P01",
        label="Period 01",
        starts_at=time(8, 0),
        ends_at=time(9, 0),
    )
    section = _section(organization=organization)
    facility = _facility()

    with pytest.raises(IntegrityError):
        Period.objects.create(
            organization=organization,
            period_code="P01",
            label="Duplicate",
            starts_at=time(9, 0),
            ends_at=time(10, 0),
        )

    with pytest.raises(IntegrityError):
        Period.objects.create(
            organization=organization,
            period_code="P02",
            label="Bad Time Window",
            starts_at=time(10, 0),
            ends_at=time(9, 0),
        )

    SectionMeetingPattern.objects.create(
        section=section,
        period=period,
        location_facility=facility,
        day_of_week=1,
        starts_at=time(8, 0),
        ends_at=time(9, 0),
    )

    with pytest.raises(IntegrityError):
        SectionMeetingPattern.objects.create(
            section=section,
            day_of_week=0,
            starts_at=time(8, 0),
            ends_at=time(9, 0),
        )

    with pytest.raises(IntegrityError):
        SectionMeetingPattern.objects.create(
            section=section,
            day_of_week=2,
            starts_at=time(9, 0),
            ends_at=time(8, 0),
        )

    with pytest.raises(IntegrityError):
        SectionMeetingPattern.objects.create(
            section=section,
            day_of_week=2,
            starts_at=time(8, 0),
            ends_at=time(9, 0),
            starts_on=date(2025, 9, 2),
            ends_on=date(2025, 9, 1),
        )
