from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class Address(BaseModel, AuditModel):
    class ValidationStatus(models.TextChoices):
        UNVALIDATED = "unvalidated", "Unvalidated"
        PARSED = "parsed", "Parsed"
        VALIDATED = "validated", "Validated"
        NEEDS_REVIEW = "needs_review", "Needs Review"
        FAILED = "failed", "Failed"

    class ValidationProvider(models.TextChoices):
        LOCAL = "local", "Local"
        GOOGLE = "google", "Google"
        USPS = "usps", "USPS"
        HYBRID = "hybrid", "Hybrid"

    raw_input = models.TextField(blank=True)
    full_address_text = models.CharField(max_length=512, blank=True)
    formatted_single_line = models.CharField(max_length=512, blank=True)
    normalized_hash = models.CharField(max_length=64, blank=True, db_index=True)
    address_number = models.CharField(max_length=20, blank=True)
    street_pre_direction = models.CharField(max_length=10, blank=True)
    street_name = models.CharField(max_length=150, blank=True)
    street_suffix = models.CharField(max_length=30, blank=True)
    street_post_direction = models.CharField(max_length=10, blank=True)
    subpremise = models.CharField(max_length=100, blank=True)
    building = models.CharField(max_length=100, blank=True)
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True)
    state_code = models.ForeignKey(
        "locations.StateCode",
        on_delete=models.PROTECT,
        related_name="addresses",
        null=True,
        blank=True,
    )
    postal_code = models.CharField(max_length=20, blank=True)
    postal_code_plus4 = models.CharField(max_length=10, blank=True)
    country_code = models.ForeignKey(
        "locations.CountryCode",
        on_delete=models.PROTECT,
        related_name="addresses",
        null=True,
        blank=True,
    )
    validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.UNVALIDATED,
    )
    validation_confidence = models.PositiveSmallIntegerField(null=True, blank=True)
    validation_provider = models.CharField(max_length=20, choices=ValidationProvider.choices, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    provider_reference = models.CharField(max_length=128, blank=True)
    validation_payload = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_address",
    )

    class Meta:
        db_table = "locations_address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=["postal_code"], name="loc_addr_postal_idx"),
            models.Index(fields=["city", "state_code"], name="loc_addr_city_state_idx"),
            models.Index(fields=["validation_status"], name="loc_addr_val_stat_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["normalized_hash"],
                condition=~Q(normalized_hash=""),
                name="loc_addr_norm_hash_uq",
            )
        ]


class AddressCatalog(BaseModel, AuditModel):
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.CASCADE,
        related_name="catalog_entries",
    )
    label = models.CharField(max_length=150)
    catalog_key = models.CharField(max_length=100, unique=True)
    normalized_hash = models.CharField(max_length=64, blank=True, db_index=True)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    match_priority = models.PositiveSmallIntegerField(default=100)
    notes = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_address_catalog",
    )

    class Meta:
        db_table = "locations_address_catalog"
        verbose_name = "Address Catalog"
        verbose_name_plural = "Address Catalog"
        ordering = ["-match_priority", "label"]


class AddressValidationRun(BaseModel, AuditModel):
    class RunStatus(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        SKIPPED = "skipped", "Skipped"

    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.CASCADE,
        related_name="validation_runs",
    )
    provider_requested = models.CharField(
        max_length=20,
        choices=Address.ValidationProvider.choices,
        default=Address.ValidationProvider.LOCAL,
    )
    status = models.CharField(max_length=20, choices=RunStatus.choices, default=RunStatus.QUEUED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result_code = models.CharField(max_length=50, blank=True)
    result_message = models.CharField(max_length=255, blank=True)
    result_payload = models.JSONField(default=dict, blank=True)
    external_cost_estimate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_locations_address_validation_run",
    )

    class Meta:
        db_table = "locations_address_validation_run"
        verbose_name = "Address Validation Run"
        verbose_name_plural = "Address Validation Runs"
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["status", "provider_requested"], name="loc_addr_val_run_st_idx"),
        ]
