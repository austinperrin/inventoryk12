from django.conf import settings
from django.db import models

from apps.common.models import AuditModel, BaseModel


class DemographicSyncModel(BaseModel, AuditModel):
    """
    Common sync metadata for demographic records.
    """

    source_system = models.CharField(max_length=100, blank=True)
    source_record_id = models.CharField(max_length=255, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class StudentDemographics(DemographicSyncModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_demographics",
    )
    student_id = models.CharField(max_length=100, blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    demographics = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "identity_student_demographics"
        verbose_name = "Student Demographics"
        verbose_name_plural = "Student Demographics"


class StaffDemographics(DemographicSyncModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_demographics",
    )
    employee_id = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    demographics = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "identity_staff_demographics"
        verbose_name = "Staff Demographics"
        verbose_name_plural = "Staff Demographics"


class GuardianDemographics(DemographicSyncModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_demographics",
    )
    guardian_id = models.CharField(max_length=100, blank=True)
    demographics = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "identity_guardian_demographics"
        verbose_name = "Guardian Demographics"
        verbose_name_plural = "Guardian Demographics"
