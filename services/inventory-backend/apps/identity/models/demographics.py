from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


class GenderCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_gender_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "identity_gender_code"
        verbose_name = "Gender Code"
        verbose_name_plural = "Gender Codes"


class RaceCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_race_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "identity_race_code"
        verbose_name = "Race Code"
        verbose_name_plural = "Race Codes"


class EthnicityCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_ethnicity_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "identity_ethnicity_code"
        verbose_name = "Ethnicity Code"
        verbose_name_plural = "Ethnicity Codes"


class PersonaDemographicsModel(BaseModel, AuditModel):
    gender = models.ForeignKey(
        "identity.GenderCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    race = models.ForeignKey(
        "identity.RaceCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    ethnicity = models.ForeignKey(
        "identity.EthnicityCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    is_native = models.BooleanField(default=False)
    is_asian = models.BooleanField(default=False)
    is_african_american = models.BooleanField(default=False)
    is_hawaiian = models.BooleanField(default=False)
    is_white = models.BooleanField(default=False)

    class Meta:
        abstract = True


class StudentDemographics(PersonaDemographicsModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_demographics",
    )
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_student_demographics",
    )

    class Meta:
        db_table = "identity_student_demographics"
        verbose_name = "Student Demographics"
        verbose_name_plural = "Student Demographics"


class StaffDemographics(PersonaDemographicsModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_demographics",
    )
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_staff_demographics",
    )

    class Meta:
        db_table = "identity_staff_demographics"
        verbose_name = "Staff Demographics"
        verbose_name_plural = "Staff Demographics"


class GuardianDemographics(PersonaDemographicsModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_demographics",
    )
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_guardian_demographics",
    )

    class Meta:
        db_table = "identity_guardian_demographics"
        verbose_name = "Guardian Demographics"
        verbose_name_plural = "Guardian Demographics"
