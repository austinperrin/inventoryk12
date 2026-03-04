from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


class OrganizationCode(CodeTableModel):
    local_id = models.CharField(max_length=64, unique=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_organization_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "organization_code"
        verbose_name = "Organization Code"
        verbose_name_plural = "Organization Codes"


class Organization(BaseModel, AuditModel):
    local_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    organization_code = models.ForeignKey(
        "organization.OrganizationCode",
        on_delete=models.PROTECT,
        related_name="organizations",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_organization",
    )

    class Meta:
        db_table = "organization"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["organization_code__sort_order", "sort_order", "name"]

    def __str__(self) -> str:
        return self.display_name or self.name


class OrganizationLifecycle(BaseModel, AuditModel):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="lifecycle_windows",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_organization_lifecycle",
    )

    class Meta:
        db_table = "organization_lifecycle"
        verbose_name = "Organization Lifecycle"
        verbose_name_plural = "Organization Lifecycles"
        ordering = ["organization_id", "starts_on"]
        indexes = [
            models.Index(
                fields=["organization", "starts_on", "ends_on"],
                name="org_lifecycle_window_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="organization_lifecycle_valid_date_window",
            )
        ]


class OrganizationAddress(BaseModel, AuditModel):
    class AddressType(models.TextChoices):
        PHYSICAL = "physical", "Physical"
        MAILING = "mailing", "Mailing"
        BILLING = "billing", "Billing"
        OTHER = "other", "Other"

    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    address_id = models.BigIntegerField(
        db_index=True,
        help_text=(
            "Placeholder contacts or locations address ID until the owning address "
            "model is established and this field can be swapped to a foreign key."
        ),
    )
    address_type = models.CharField(
        max_length=20,
        choices=AddressType.choices,
        default=AddressType.PHYSICAL,
    )
    is_primary = models.BooleanField(default=False)
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_organization_address",
    )

    class Meta:
        db_table = "organization_address"
        verbose_name = "Organization Address"
        verbose_name_plural = "Organization Addresses"
        indexes = [
            models.Index(
                fields=["organization", "address_type", "is_primary"],
                name="org_address_primary_idx",
            ),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="organization_address_valid_date_window",
            ),
            models.UniqueConstraint(
                fields=["organization", "address_id", "address_type"],
                name="organization_address_unique_link",
            ),
        ]


class OrganizationAdditionalIdentifier(BaseModel, AuditModel):
    organization = models.ForeignKey(
        "organization.Organization",
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
        table_name="hist_organization_additional_identifier",
    )

    class Meta:
        db_table = "organization_additional_identifier"
        verbose_name = "Organization Additional Identifier"
        verbose_name_plural = "Organization Additional Identifiers"
        indexes = [
            models.Index(
                fields=["organization", "system", "identifier_type"],
                name="org_addid_lookup_idx",
            ),
            models.Index(fields=["identifier_value"], name="org_addid_value_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="organization_additional_id_valid_date_window",
            ),
            models.UniqueConstraint(
                fields=["organization", "system", "identifier_type", "identifier_value"],
                name="organization_additional_id_unique_value",
            ),
        ]
