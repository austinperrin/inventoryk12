from django.db import models
from django.db.models import Q

from apps.common.models import AuditModel, BaseModel


class AcademicYear(BaseModel, AuditModel):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    code = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    org_unit_id = models.UUIDField(null=True, blank=True, db_index=True)
    starts_on = models.DateField()
    ends_on = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = "academic_year"
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__gte=models.F("starts_on")),
                name="academic_year_valid_date_window",
            )
        ]

    def __str__(self) -> str:
        return self.label


class AcademicCalendar(BaseModel, AuditModel):
    academic_year = models.ForeignKey(
        "academic.AcademicYear",
        on_delete=models.CASCADE,
        related_name="calendars",
    )
    org_unit_id = models.UUIDField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "academic_calendar"
        verbose_name = "Academic Calendar"
        verbose_name_plural = "Academic Calendars"

    def __str__(self) -> str:
        return self.name


class AcademicCalendarDay(BaseModel, AuditModel):
    calendar = models.ForeignKey(
        "academic.AcademicCalendar",
        on_delete=models.CASCADE,
        related_name="days",
    )
    day_on = models.DateField()
    is_instructional = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "academic_calendar_day"
        verbose_name = "Academic Calendar Day"
        verbose_name_plural = "Academic Calendar Days"
        constraints = [
            models.UniqueConstraint(
                fields=["calendar", "day_on"],
                name="academic_calendar_day_unique_day_per_calendar",
            )
        ]


class AcademicTerm(BaseModel, AuditModel):
    class TermType(models.TextChoices):
        YEAR = "year", "Year"
        SEMESTER = "semester", "Semester"
        QUARTER = "quarter", "Quarter"
        GRADING_PERIOD = "grading_period", "Grading Period"
        CYCLE = "cycle", "Cycle"
        CUSTOM = "custom", "Custom"

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
    org_unit_id = models.UUIDField(null=True, blank=True, db_index=True)
    term_type = models.CharField(max_length=30, choices=TermType.choices, default=TermType.CUSTOM)
    code = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=100)
    starts_on = models.DateField()
    ends_on = models.DateField()

    class Meta:
        db_table = "academic_term"
        verbose_name = "Academic Term"
        verbose_name_plural = "Academic Terms"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__gte=models.F("starts_on")),
                name="academic_term_valid_date_window",
            )
        ]

    def __str__(self) -> str:
        return self.label
