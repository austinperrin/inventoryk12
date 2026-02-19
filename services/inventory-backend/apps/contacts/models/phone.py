from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class PhoneCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_phone_code",
    )

    class Meta:
        db_table = "contacts_phone_code"
        verbose_name = "Phone Code"
        verbose_name_plural = "Phone Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.label or self.code


class Phone(BaseModel, AuditModel):
    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="phones",
    )
    phone_number = models.CharField(max_length=32)
    extension = models.CharField(max_length=16, blank=True)
    phone_code = models.ForeignKey(
        "contacts.PhoneCode",
        on_delete=models.PROTECT,
        related_name="phones",
    )
    is_primary = models.BooleanField(default=False)
    is_sms_capable = models.BooleanField(default=False)
    is_sms_opted_out = models.BooleanField(default=False)
    sms_opted_out_at = models.DateTimeField(null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_phone",
    )

    class Meta:
        db_table = "contacts_phone"
        verbose_name = "Phone"
        verbose_name_plural = "Phones"
        ordering = ["user_id", "sort_order", "-is_primary", "id"]
        indexes = [
            models.Index(fields=["user", "is_sms_opted_out"], name="ct_usr_ph_sms_opt_idx"),
            models.Index(fields=["user", "is_primary"], name="ct_usr_ph_user_pri_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "phone_number", "phone_code"],
                name="ct_usr_ph_unique_val",
            )
        ]
