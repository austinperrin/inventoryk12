from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class PrefixCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_prefix_code",
    )

    class Meta:
        db_table = "identity_prefix_code"
        verbose_name = "Prefix Code"
        verbose_name_plural = "Prefix Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.display_name or self.code


class SuffixCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_suffix_code",
    )

    class Meta:
        db_table = "identity_suffix_code"
        verbose_name = "Suffix Code"
        verbose_name_plural = "Suffix Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.display_name or self.code


class PersonaDetailModel(BaseModel, AuditModel):
    prefix = models.ForeignKey(
        "identity.PrefixCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    suffix = models.ForeignKey(
        "identity.SuffixCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    birth_country = models.ForeignKey(
        "contacts.CountryCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    birth_state = models.ForeignKey(
        "contacts.StateCode",
        on_delete=models.PROTECT,
        related_name="%(class)s_records",
        null=True,
        blank=True,
    )
    birth_city = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True


class StudentDetail(PersonaDetailModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_detail",
    )
    local_id = models.CharField(max_length=64, blank=True, db_index=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_student_detail",
    )

    class Meta:
        db_table = "identity_student_detail"
        verbose_name = "Student Detail"
        verbose_name_plural = "Student Details"


class StaffDetail(PersonaDetailModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_detail",
    )
    local_id = models.CharField(max_length=64, blank=True, db_index=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_staff_detail",
    )

    class Meta:
        db_table = "identity_staff_detail"
        verbose_name = "Staff Detail"
        verbose_name_plural = "Staff Details"


class GuardianDetail(PersonaDetailModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_detail",
    )
    local_id = models.CharField(max_length=64, blank=True, db_index=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_guardian_detail",
    )

    class Meta:
        db_table = "identity_guardian_detail"
        verbose_name = "Guardian Detail"
        verbose_name_plural = "Guardian Details"
