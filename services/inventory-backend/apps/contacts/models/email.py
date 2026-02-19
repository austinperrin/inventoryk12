from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class EmailCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_email_code",
    )

    class Meta:
        db_table = "contacts_email_code"
        verbose_name = "Email Code"
        verbose_name_plural = "Email Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.label or self.code


class Email(BaseModel, AuditModel):
    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="emails",
    )
    email_address = models.EmailField(max_length=255)
    email_code = models.ForeignKey(
        "contacts.EmailCode",
        on_delete=models.PROTECT,
        related_name="emails",
    )
    is_primary = models.BooleanField(default=False)
    is_notification_enabled = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_email",
    )

    class Meta:
        db_table = "contacts_email"
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ["user_id", "sort_order", "-is_primary", "id"]
        indexes = [
            models.Index(fields=["user", "is_primary"], name="ct_usr_em_user_pri_idx"),
            models.Index(fields=["user", "is_notification_enabled"], name="ct_usr_em_notif_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "email_address", "email_code"],
                name="ct_usr_em_unique_val",
            )
        ]
