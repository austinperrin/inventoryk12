from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


class SubjectCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_subject_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "instruction_subject_code"
        verbose_name = "Subject Code"
        verbose_name_plural = "Subject Codes"


class GradeLevelCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_grade_level_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "instruction_grade_level_code"
        verbose_name = "Grade Level Code"
        verbose_name_plural = "Grade Level Codes"


class Course(BaseModel, AuditModel):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="courses",
    )
    course_code = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject_code = models.ForeignKey(
        "instruction.SubjectCode",
        on_delete=models.PROTECT,
        related_name="courses",
    )
    grade_low_code = models.ForeignKey(
        "instruction.GradeLevelCode",
        on_delete=models.PROTECT,
        related_name="courses_as_grade_low",
        null=True,
        blank=True,
    )
    grade_high_code = models.ForeignKey(
        "instruction.GradeLevelCode",
        on_delete=models.PROTECT,
        related_name="courses_as_grade_high",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_course",
    )

    class Meta:
        db_table = "instruction_course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["organization_id", "course_code", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "course_code"],
                name="ins_course_unique_org_code",
            )
        ]

    def __str__(self) -> str:
        return f"{self.course_code} - {self.title}"


class CourseAdditionalIdentifier(BaseModel, AuditModel):
    course = models.ForeignKey(
        "instruction.Course",
        on_delete=models.CASCADE,
        related_name="additional_ids",
    )
    system = models.CharField(max_length=50)
    identifier_type = models.CharField(max_length=50)
    identifier_value = models.CharField(max_length=255)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_course_additional_identifier",
    )

    class Meta:
        db_table = "instruction_course_additional_identifier"
        verbose_name = "Course Additional Identifier"
        verbose_name_plural = "Course Additional Identifiers"
        indexes = [
            models.Index(
                fields=["course", "system", "identifier_type"],
                name="ins_course_addid_lookup_idx",
            ),
            models.Index(fields=["identifier_value"], name="ins_course_addid_val_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ins_course_addid_valid_win",
            ),
            models.UniqueConstraint(
                fields=["course", "system", "identifier_type", "identifier_value"],
                name="ins_course_addid_unique_val",
            ),
        ]


class Section(BaseModel, AuditModel):
    course = models.ForeignKey(
        "instruction.Course",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    academic_term = models.ForeignKey(
        "academic.AcademicTerm",
        on_delete=models.PROTECT,
        related_name="sections",
    )
    section_code = models.CharField(max_length=64)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_section",
    )

    class Meta:
        db_table = "instruction_section"
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        ordering = ["organization_id", "academic_term_id", "section_code", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ins_section_valid_win",
            ),
            models.UniqueConstraint(
                fields=["organization", "academic_term", "section_code"],
                name="ins_section_unique_org_term_code",
            ),
        ]

    def __str__(self) -> str:
        return self.section_code


class SectionAdditionalIdentifier(BaseModel, AuditModel):
    section = models.ForeignKey(
        "instruction.Section",
        on_delete=models.CASCADE,
        related_name="additional_ids",
    )
    system = models.CharField(max_length=50)
    identifier_type = models.CharField(max_length=50)
    identifier_value = models.CharField(max_length=255)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_section_additional_identifier",
    )

    class Meta:
        db_table = "instruction_section_additional_identifier"
        verbose_name = "Section Additional Identifier"
        verbose_name_plural = "Section Additional Identifiers"
        indexes = [
            models.Index(
                fields=["section", "system", "identifier_type"],
                name="ins_section_addid_lookup_idx",
            ),
            models.Index(fields=["identifier_value"], name="ins_section_addid_val_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ins_section_addid_valid_win",
            ),
            models.UniqueConstraint(
                fields=["section", "system", "identifier_type", "identifier_value"],
                name="ins_section_addid_unique_val",
            ),
        ]


class Period(BaseModel, AuditModel):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="periods",
    )
    facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.SET_NULL,
        related_name="periods",
        null=True,
        blank=True,
    )
    period_code = models.CharField(max_length=64)
    label = models.CharField(max_length=100)
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_period",
    )

    class Meta:
        db_table = "instruction_period"
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ["organization_id", "sort_order", "period_code", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_at__gt=models.F("starts_at")),
                name="ins_period_valid_time_win",
            ),
            models.UniqueConstraint(
                fields=["organization", "period_code"],
                name="ins_period_unique_org_code",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.period_code} - {self.label}"


class SectionMeetingPattern(BaseModel, AuditModel):
    section = models.ForeignKey(
        "instruction.Section",
        on_delete=models.CASCADE,
        related_name="meeting_patterns",
    )
    period = models.ForeignKey(
        "instruction.Period",
        on_delete=models.SET_NULL,
        related_name="meeting_patterns",
        null=True,
        blank=True,
    )
    location_facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.SET_NULL,
        related_name="meeting_patterns",
        null=True,
        blank=True,
    )
    day_of_week = models.PositiveSmallIntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    cycle_day = models.CharField(max_length=20, blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_instruction_section_meeting_pattern",
    )

    class Meta:
        db_table = "instruction_section_meeting_pattern"
        verbose_name = "Section Meeting Pattern"
        verbose_name_plural = "Section Meeting Patterns"
        ordering = ["section_id", "day_of_week", "starts_at", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(day_of_week__gte=1) & Q(day_of_week__lte=7),
                name="ins_meeting_day_valid_range",
            ),
            models.CheckConstraint(
                condition=Q(ends_at__gt=models.F("starts_at")),
                name="ins_meeting_valid_time_win",
            ),
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ins_meeting_valid_date_win",
            ),
        ]
