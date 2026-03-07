from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


def _window_overlap_q(*, starts_on, ends_on):
    overlap = Q(ends_on__isnull=True) | Q(ends_on__gte=starts_on)
    if ends_on is not None:
        overlap &= Q(starts_on__lte=ends_on)
    return overlap


class EnrollmentEntryCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_entry_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "enrollment_entry_code"
        verbose_name = "Enrollment Entry Code"
        verbose_name_plural = "Enrollment Entry Codes"


class EnrollmentExitCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_exit_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "enrollment_exit_code"
        verbose_name = "Enrollment Exit Code"
        verbose_name_plural = "Enrollment Exit Codes"


class StaffAssignmentRoleCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_staff_assignment_role_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "enrollment_staff_assignment_role_code"
        verbose_name = "Staff Assignment Role Code"
        verbose_name_plural = "Staff Assignment Role Codes"


class StudentEnrollment(BaseModel, AuditModel):
    student_user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="student_enrollments",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="student_enrollments",
    )
    grade_level_code = models.ForeignKey(
        "instruction.GradeLevelCode",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    entry_code = models.ForeignKey(
        "enrollment.EnrollmentEntryCode",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
        null=True,
        blank=True,
    )
    exit_code = models.ForeignKey(
        "enrollment.EnrollmentExitCode",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
        null=True,
        blank=True,
    )
    role_assignment = models.ForeignKey(
        "identity.RoleAssignment",
        on_delete=models.SET_NULL,
        related_name="student_enrollment_links",
        null=True,
        blank=True,
    )
    role_assignment_org = models.ForeignKey(
        "identity.RoleAssignmentOrganization",
        on_delete=models.SET_NULL,
        related_name="student_enrollment_links",
        null=True,
        blank=True,
    )
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_student_enrollment",
    )

    class Meta:
        db_table = "enrollment_student_enrollment"
        verbose_name = "Student Enrollment"
        verbose_name_plural = "Student Enrollments"
        ordering = ["organization_id", "student_user_id", "starts_on", "id"]
        indexes = [
            models.Index(
                fields=["student_user", "organization", "starts_on", "ends_on"],
                name="enr_student_enroll_window_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="enr_student_enroll_valid_win",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if self.role_assignment and self.role_assignment.user_id != self.student_user_id:
            raise ValidationError(
                {"role_assignment": "Role assignment must belong to the student user."}
            )

        if (
            self.role_assignment_org
            and self.role_assignment
            and self.role_assignment_org.role_assignment_id != self.role_assignment_id
        ):
            raise ValidationError(
                {"role_assignment_org": "Role assignment organization must match role assignment."}
            )

        if (
            self.role_assignment_org
            and self.role_assignment_org.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "role_assignment_org": "Role assignment organization must match enrollment organization."
                }
            )

        overlapping = (
            StudentEnrollment.objects.filter(
                student_user=self.student_user,
                organization=self.organization,
            )
            .exclude(pk=self.pk)
            .filter(_window_overlap_q(starts_on=self.starts_on, ends_on=self.ends_on))
        )
        if overlapping.exists():
            raise ValidationError(
                {
                    "starts_on": "Overlapping student enrollment windows are not allowed for this scope."
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class StudentSchedule(BaseModel, AuditModel):
    section = models.ForeignKey(
        "instruction.Section",
        on_delete=models.CASCADE,
        related_name="student_schedules",
    )
    student_user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="student_schedules",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    entry_code = models.ForeignKey(
        "enrollment.EnrollmentEntryCode",
        on_delete=models.PROTECT,
        related_name="student_schedules",
        null=True,
        blank=True,
    )
    exit_code = models.ForeignKey(
        "enrollment.EnrollmentExitCode",
        on_delete=models.PROTECT,
        related_name="student_schedules",
        null=True,
        blank=True,
    )
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_student_schedule",
    )

    class Meta:
        db_table = "enrollment_student_schedule"
        verbose_name = "Student Schedule"
        verbose_name_plural = "Student Schedules"
        ordering = ["section_id", "student_user_id", "starts_on", "id"]
        indexes = [
            models.Index(
                fields=["student_user", "section", "starts_on", "ends_on"],
                name="enr_student_sched_window_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="enr_student_sched_valid_win",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        if self.section.starts_on and self.starts_on < self.section.starts_on:
            raise ValidationError(
                {"starts_on": "Student schedule start date must be on or after section start date."}
            )

        if self.ends_on and self.section.ends_on and self.ends_on > self.section.ends_on:
            raise ValidationError(
                {"ends_on": "Student schedule end date must be on or before section end date."}
            )

        overlapping = (
            StudentSchedule.objects.filter(
                student_user=self.student_user,
                section=self.section,
            )
            .exclude(pk=self.pk)
            .filter(_window_overlap_q(starts_on=self.starts_on, ends_on=self.ends_on))
        )
        if overlapping.exists():
            raise ValidationError(
                {
                    "starts_on": "Overlapping student schedule windows are not allowed for this scope."
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class StaffSchedule(BaseModel, AuditModel):
    section = models.ForeignKey(
        "instruction.Section",
        on_delete=models.CASCADE,
        related_name="staff_schedules",
    )
    staff_user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="staff_schedules",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    staff_assignment_role_code = models.ForeignKey(
        "enrollment.StaffAssignmentRoleCode",
        on_delete=models.PROTECT,
        related_name="staff_schedules",
        null=True,
        blank=True,
    )
    is_primary = models.BooleanField(default=False)
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_enrollment_staff_schedule",
    )

    class Meta:
        db_table = "enrollment_staff_schedule"
        verbose_name = "Staff Schedule"
        verbose_name_plural = "Staff Schedules"
        ordering = ["section_id", "staff_user_id", "starts_on", "id"]
        indexes = [
            models.Index(
                fields=["staff_user", "section", "starts_on", "ends_on"],
                name="enr_staff_sched_window_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="enr_staff_sched_valid_win",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        if self.section.starts_on and self.starts_on < self.section.starts_on:
            raise ValidationError(
                {"starts_on": "Staff schedule start date must be on or after section start date."}
            )

        if self.ends_on and self.section.ends_on and self.ends_on > self.section.ends_on:
            raise ValidationError(
                {"ends_on": "Staff schedule end date must be on or before section end date."}
            )

        overlapping = (
            StaffSchedule.objects.filter(
                staff_user=self.staff_user,
                section=self.section,
            )
            .exclude(pk=self.pk)
            .filter(_window_overlap_q(starts_on=self.starts_on, ends_on=self.ends_on))
        )
        if overlapping.exists():
            raise ValidationError(
                {"starts_on": "Overlapping staff schedule windows are not allowed for this scope."}
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
