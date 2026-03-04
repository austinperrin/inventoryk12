from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class UserAdditionalIdentifier(BaseModel, AuditModel):
    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="additional_ids",
    )
    system = models.CharField(max_length=50)
    identifier_type = models.CharField(max_length=50)
    identifier_value = models.CharField(max_length=255)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_user_additional_identifier",
    )

    class Meta:
        db_table = "identity_user_additional_identifier"
        verbose_name = "User Additional Identifier"
        verbose_name_plural = "User Additional Identifiers"
        indexes = [
            models.Index(
                fields=["user", "system", "identifier_type"],
                name="id_usr_addid_lookup_idx",
            ),
            models.Index(fields=["identifier_value"], name="id_usr_addid_value_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "system", "identifier_type", "identifier_value"],
                name="identity_user_additional_id_unique_value",
            ),
        ]
