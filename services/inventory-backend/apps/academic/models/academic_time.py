from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


class AcademicYear(BaseModel, AuditModel):
    year_code = models.PositiveIntegerField()
    label = models.CharField(max_length=50)
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="academic_years",
        null=True,
        blank=True,
    )
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
        ordering = ["organization_id", "year_code", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(starts_on__isnull=True)
                | Q(ends_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="acad_year_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["organization", "year_code"],
                name="acad_year_unique_org_code",
            ),
            models.UniqueConstraint(
                fields=["organization"],
                condition=Q(is_current=True),
                name="acad_year_single_current",
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
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="academic_calendars",
        null=True,
        blank=True,
    )
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
        ordering = ["academic_year_id", "organization_id", "name", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "organization", "name"],
                name="acad_cal_unique_org_name",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class AcademicTermCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_academic_term_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "academic_term_code"
        verbose_name = "Academic Term Code"
        verbose_name_plural = "Academic Term Codes"


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
        ordering = ["calendar_id", "starts_on", "title", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__gte=models.F("starts_on")),
                name="acad_cal_evt_valid_date_win",
            ),
        ]


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
        ordering = ["calendar_id", "calendar_date", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["calendar", "calendar_date"],
                name="acad_cal_day_unique_date",
            ),
        ]


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
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="academic_terms",
        null=True,
        blank=True,
    )
    term_code = models.ForeignKey(
        "academic.AcademicTermCode",
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
        ordering = ["academic_year_id", "starts_on", "id"]
        indexes = [
            models.Index(
                fields=["academic_year", "starts_on", "ends_on"], name="acad_term_window_idx"
            ),
            models.Index(
                fields=["organization", "starts_on", "ends_on"], name="acad_term_org_win_idx"
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__gte=models.F("starts_on")),
                name="acad_term_valid_date_win",
            ),
            models.CheckConstraint(
                condition=~Q(parent_term=models.F("id")),
                name="acad_term_not_self_parent",
            ),
            models.UniqueConstraint(
                fields=["academic_year", "term_code", "code"],
                condition=~Q(code=""),
                name="acad_term_unique_code",
            ),
        ]

    def __str__(self) -> str:
        return self.label
