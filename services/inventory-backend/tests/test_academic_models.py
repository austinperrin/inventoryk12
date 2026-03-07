from datetime import date

import pytest
from django.db import IntegrityError

from apps.academic.models import (
    AcademicCalendar,
    AcademicCalendarDay,
    AcademicCalendarEvent,
    AcademicTerm,
    AcademicTermCode,
    AcademicYear,
)
from apps.organization.models import Organization, OrganizationCode


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


def _calendar(**overrides):
    academic_year = overrides.pop("academic_year", None) or _academic_year()
    data = {
        "academic_year": academic_year,
        "organization": academic_year.organization,
        "name": "Default Calendar",
        "is_default": True,
    }
    data.update(overrides)
    return AcademicCalendar.objects.create(**data)


def _term_code(**overrides):
    data = {
        "code": "semester",
        "label": "Semester",
        "sort_order": 10,
    }
    data.update(overrides)
    return AcademicTermCode.objects.create(**data)


@pytest.mark.django_db(transaction=True)
def test_academic_year_rejects_invalid_date_window() -> None:
    organization = _organization()

    with pytest.raises(IntegrityError):
        AcademicYear.objects.create(
            year_code=2026,
            label="2025-2026",
            organization=organization,
            starts_on=date(2026, 6, 1),
            ends_on=date(2026, 5, 31),
        )


@pytest.mark.django_db(transaction=True)
def test_academic_year_allows_single_current_per_organization() -> None:
    organization = _organization()
    AcademicYear.objects.create(
        year_code=2025,
        label="2024-2025",
        organization=organization,
        is_current=True,
    )

    with pytest.raises(IntegrityError):
        AcademicYear.objects.create(
            year_code=2026,
            label="2025-2026",
            organization=organization,
            is_current=True,
        )


@pytest.mark.django_db(transaction=True)
def test_academic_calendar_unique_name_per_org_and_year() -> None:
    academic_year = _academic_year()
    AcademicCalendar.objects.create(
        academic_year=academic_year,
        organization=academic_year.organization,
        name="Instructional",
    )

    with pytest.raises(IntegrityError):
        AcademicCalendar.objects.create(
            academic_year=academic_year,
            organization=academic_year.organization,
            name="Instructional",
        )


@pytest.mark.django_db(transaction=True)
def test_academic_calendar_event_rejects_invalid_date_window() -> None:
    calendar = _calendar()

    with pytest.raises(IntegrityError):
        AcademicCalendarEvent.objects.create(
            calendar=calendar,
            title="Bad Window",
            starts_on=date(2025, 9, 2),
            ends_on=date(2025, 9, 1),
        )


@pytest.mark.django_db(transaction=True)
def test_academic_calendar_day_unique_per_calendar_date() -> None:
    calendar = _calendar()
    AcademicCalendarDay.objects.create(
        calendar=calendar,
        calendar_date=date(2025, 9, 1),
        is_workday=True,
        is_instructional=True,
    )

    with pytest.raises(IntegrityError):
        AcademicCalendarDay.objects.create(
            calendar=calendar,
            calendar_date=date(2025, 9, 1),
            is_workday=True,
            is_instructional=True,
        )


@pytest.mark.django_db(transaction=True)
def test_academic_term_requires_valid_window_and_unique_non_empty_code() -> None:
    academic_year = _academic_year()
    term_code = _term_code()
    AcademicTerm.objects.create(
        academic_year=academic_year,
        organization=academic_year.organization,
        term_code=term_code,
        code="FALL",
        label="Fall Semester",
        starts_on=date(2025, 8, 1),
        ends_on=date(2025, 12, 20),
    )

    with pytest.raises(IntegrityError):
        AcademicTerm.objects.create(
            academic_year=academic_year,
            organization=academic_year.organization,
            term_code=term_code,
            code="FALL",
            label="Duplicate Fall",
            starts_on=date(2025, 8, 1),
            ends_on=date(2025, 12, 20),
        )

    with pytest.raises(IntegrityError):
        AcademicTerm.objects.create(
            academic_year=academic_year,
            organization=academic_year.organization,
            term_code=term_code,
            code="",
            label="Bad Dates",
            starts_on=date(2025, 12, 20),
            ends_on=date(2025, 8, 1),
        )
