from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class AcademicYear(BaseModel, AuditModel):
    year_code = models.PositiveIntegerField()
    label = models.CharField(max_length=50)
    organization_id = models.UUIDField(null=True, blank=True, db_index=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_current = models.BooleanField(default=False)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_year",
    )

    class Meta:
        db_table = "academic_year"
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
        constraints = [
            models.CheckConstraint(
                check=Q(starts_on__isnull=True)
                | Q(ends_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="academic_year_valid_date_window",
            ),
            models.UniqueConstraint(
                fields=["year_code"],
                name="academic_year_unique_year_code",
            ),
            models.UniqueConstraint(
                fields=["is_current"],
                condition=Q(is_current=True),
                name="academic_year_single_current",
            ),
        ]

    def __str__(self) -> str:
        return self.label


class AcademicCalendar(BaseModel, AuditModel):
    academic_year = models.ForeignKey(
        "academic.AcademicYear",
        on_delete=models.CASCADE,
        related_name="calendars",
    )
    organization_id = models.UUIDField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_calendar",
    )

    class Meta:
        db_table = "academic_calendar"
        verbose_name = "Academic Calendar"
        verbose_name_plural = "Academic Calendars"
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "organization_id", "name"],
                name="academic_calendar_unique_name_per_org_year",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class AcademicTermTypeCode(BaseModel, AuditModel):
    code = models.CharField(max_length=50)
    label = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_term_type_code",
    )

    class Meta:
        db_table = "academic_term_type_code"
        verbose_name = "Academic Term Type Code"
        verbose_name_plural = "Academic Term Type Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.label or self.code


class AcademicCalendarEvent(BaseModel, AuditModel):
    calendar = models.ForeignKey(
        "academic.AcademicCalendar",
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    starts_on = models.DateField()
    ends_on = models.DateField()
    is_public = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_calendar_event",
    )

    class Meta:
        db_table = "academic_calendar_event"
        verbose_name = "Academic Calendar Event"
        verbose_name_plural = "Academic Calendar Events"
        ordering = ["calendar_id", "starts_on", "title"]
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__gte=models.F("starts_on")),
                name="academic_calendar_event_valid_date_window",
            )
        ]

    def clean(self) -> None:
        super().clean()
        academic_year = self.calendar.academic_year
        if (
            academic_year.starts_on is not None
            and academic_year.ends_on is not None
            and (self.starts_on < academic_year.starts_on or self.ends_on > academic_year.ends_on)
        ):
            raise ValidationError(
                {"starts_on": "Event dates must fall within the linked academic year window."}
            )


class AcademicCalendarDay(BaseModel, AuditModel):
    calendar = models.ForeignKey(
        "academic.AcademicCalendar",
        on_delete=models.CASCADE,
        related_name="days",
    )
    calendar_date = models.DateField()
    is_workday = models.BooleanField(default=False)
    is_instructional = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_calendar_day",
    )

    class Meta:
        db_table = "academic_calendar_day"
        verbose_name = "Academic Calendar Day"
        verbose_name_plural = "Academic Calendar Days"
        constraints = [
            models.UniqueConstraint(
                fields=["calendar", "calendar_date"],
                name="academic_calendar_day_unique_day_per_calendar",
            )
        ]

    def clean(self) -> None:
        super().clean()
        academic_year = self.calendar.academic_year
        if (
            academic_year.starts_on is not None
            and academic_year.ends_on is not None
            and (
                self.calendar_date < academic_year.starts_on
                or self.calendar_date > academic_year.ends_on
            )
        ):
            raise ValidationError(
                {"calendar_date": "Calendar day must fall within the linked academic year window."}
            )


class AcademicTerm(BaseModel, AuditModel):
    academic_year = models.ForeignKey(
        "academic.AcademicYear",
        on_delete=models.CASCADE,
        related_name="terms",
    )
    calendar = models.ForeignKey(
        "academic.AcademicCalendar",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terms",
    )
    parent_term = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_terms",
    )
    organization_id = models.UUIDField(null=True, blank=True, db_index=True)
    term_type_code = models.ForeignKey(
        "academic.AcademicTermTypeCode",
        on_delete=models.PROTECT,
        related_name="terms",
    )
    code = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=100)
    starts_on = models.DateField()
    ends_on = models.DateField()
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_term",
    )

    class Meta:
        db_table = "academic_term"
        verbose_name = "Academic Term"
        verbose_name_plural = "Academic Terms"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__gte=models.F("starts_on")),
                name="academic_term_valid_date_window",
            ),
            models.UniqueConstraint(
                fields=["academic_year", "term_type_code", "code"],
                condition=~Q(code=""),
                name="academic_term_unique_code_in_year",
            ),
        ]

    def __str__(self) -> str:
        return self.label

    def clean(self) -> None:
        super().clean()
        if (
            self.academic_year.starts_on is not None
            and self.academic_year.ends_on is not None
            and (self.starts_on < self.academic_year.starts_on or self.ends_on > self.academic_year.ends_on)
        ):
            raise ValidationError(
                {"starts_on": "Term dates must fall within the linked academic year window."}
            )

        if self.calendar and self.calendar.academic_year_id != self.academic_year_id:
            raise ValidationError(
                {"calendar": "Selected calendar must belong to the same academic year as the term."}
            )

        if self.parent_term:
            if self.parent_term.academic_year_id != self.academic_year_id:
                raise ValidationError(
                    {"parent_term": "Parent term must belong to the same academic year."}
                )
            if self.starts_on < self.parent_term.starts_on or self.ends_on > self.parent_term.ends_on:
                raise ValidationError(
                    {"starts_on": "Child term dates must fall within the parent term window."}
                )
