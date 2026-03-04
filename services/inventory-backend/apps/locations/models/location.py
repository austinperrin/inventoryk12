from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel, CodeTableModel


class CountryCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_country_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "locations_country_code"
        verbose_name = "Country Code"
        verbose_name_plural = "Country Codes"


class StateCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_state_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "locations_state_code"
        verbose_name = "State Code"
        verbose_name_plural = "State Codes"


class FacilityCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_facility_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "locations_facility_code"
        verbose_name = "Facility Code"
        verbose_name_plural = "Facility Codes"


class AddressCode(CodeTableModel):
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_address_code",
    )

    class Meta(CodeTableModel.Meta):
        db_table = "locations_address_code"
        verbose_name = "Address Code"
        verbose_name_plural = "Address Codes"


class Facility(BaseModel, AuditModel):
    local_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    facility_code = models.ForeignKey(
        "locations.FacilityCode",
        on_delete=models.PROTECT,
        related_name="facilities",
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
        table_name="hist_locations_facility",
    )

    class Meta:
        db_table = "locations_facility"
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"
        ordering = ["facility_code__sort_order", "sort_order", "name"]

    def __str__(self) -> str:
        return self.display_name or self.name


class FacilityDetail(BaseModel, AuditModel):
    facility = models.OneToOneField(
        "locations.Facility",
        on_delete=models.CASCADE,
        related_name="detail",
    )
    floor_plan_url = models.URLField(blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    delivery_instructions = models.CharField(max_length=255, blank=True)
    website_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_facility_detail",
    )

    class Meta:
        db_table = "locations_facility_detail"
        verbose_name = "Facility Detail"
        verbose_name_plural = "Facility Details"


class FacilityLifecycle(BaseModel, AuditModel):
    facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.CASCADE,
        related_name="lifecycle_windows",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_facility_lifecycle",
    )

    class Meta:
        db_table = "locations_facility_lifecycle"
        verbose_name = "Facility Lifecycle"
        verbose_name_plural = "Facility Lifecycles"
        ordering = ["facility_id", "starts_on"]
        indexes = [
            models.Index(fields=["facility", "starts_on", "ends_on"], name="fac_lifecycle_window_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="fac_lifecycle_valid_win",
            )
        ]


class FacilityAddress(BaseModel, AuditModel):
    facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.CASCADE,
        related_name="facility_links",
    )
    address_code = models.ForeignKey(
        "locations.AddressCode",
        on_delete=models.PROTECT,
        related_name="facility_addresses",
    )
    is_primary = models.BooleanField(default=False)
    source_system = models.CharField(max_length=50, blank=True)
    source_record_id = models.CharField(max_length=128, blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_facility_address",
    )

    class Meta:
        db_table = "locations_facility_address"
        verbose_name = "Facility Address"
        verbose_name_plural = "Facility Addresses"
        indexes = [
            models.Index(fields=["facility", "address_code", "is_primary"], name="fac_addr_primary_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="fac_addr_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["facility", "address", "address_code"],
                name="fac_addr_unique_link",
            ),
        ]


class OrganizationFacility(BaseModel, AuditModel):
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="facility_links",
    )
    facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.CASCADE,
        related_name="organization_links",
    )
    is_primary = models.BooleanField(default=False)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_org_facility",
    )

    class Meta:
        db_table = "locations_organization_facility"
        verbose_name = "Organization Facility"
        verbose_name_plural = "Organization Facilities"
        indexes = [
            models.Index(fields=["organization", "starts_on", "ends_on"], name="fac_org_link_org_win_idx"),
            models.Index(fields=["facility", "starts_on", "ends_on"], name="fac_org_link_fac_win_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="fac_org_link_valid_win",
            ),
        ]


class FacilityAdditionalIdentifier(BaseModel, AuditModel):
    facility = models.ForeignKey(
        "locations.Facility",
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
        table_name="hist_locations_facility_additional_identifier",
    )

    class Meta:
        db_table = "locations_facility_additional_identifier"
        verbose_name = "Facility Additional Identifier"
        verbose_name_plural = "Facility Additional Identifiers"
        indexes = [
            models.Index(fields=["facility", "system", "identifier_type"], name="fac_addid_lookup_idx"),
            models.Index(fields=["identifier_value"], name="fac_addid_value_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="fac_addl_id_valid_win",
            ),
            models.UniqueConstraint(
                fields=["facility", "system", "identifier_type", "identifier_value"],
                name="fac_addl_id_unique_value",
            ),
        ]
