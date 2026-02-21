from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class UserAddress(BaseModel, AuditModel):
    class AddressType(models.TextChoices):
        PHYSICAL = "physical", "Physical"
        MAILING = "mailing", "Mailing"
        BILLING = "billing", "Billing"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="address_links",
    )
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.CASCADE,
        related_name="user_links",
    )
    address_type = models.CharField(max_length=20, choices=AddressType.choices, default=AddressType.PHYSICAL)
    is_primary = models.BooleanField(default=False)
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_user_address",
    )

    class Meta:
        db_table = "contacts_user_address"
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ct_usr_addr_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["user", "address", "address_type"],
                name="ct_usr_addr_unique_link",
            ),
            models.UniqueConstraint(
                fields=["user", "address_type"],
                condition=Q(is_primary=True),
                name="ct_usr_addr_primary_per_type",
            ),
        ]
