from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class CountryCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_country_code",
    )

    class Meta:
        db_table = "contacts_country_code"
        verbose_name = "Country Code"
        verbose_name_plural = "Country Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.display_name or self.code


class StateCode(BaseModel, AuditModel):
    code = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_state_code",
    )

    class Meta:
        db_table = "contacts_state_code"
        verbose_name = "State Code"
        verbose_name_plural = "State Codes"
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.display_name or self.code
