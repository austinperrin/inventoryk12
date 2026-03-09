from django.contrib.auth.models import Group
from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class MfaPolicy(BaseModel, AuditModel):
    policy_key = models.CharField(max_length=32, unique=True, default="default")
    enforce_for_all = models.BooleanField(default=False)
    allow_user_opt_in = models.BooleanField(default=True)
    enforced_roles = models.ManyToManyField(
        Group,
        blank=True,
        related_name="identity_mfa_policies",
    )
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_mfa_policy",
    )

    class Meta:
        db_table = "identity_mfa_policy"
        verbose_name = "MFA Policy"
        verbose_name_plural = "MFA Policies"

    def __str__(self) -> str:
        return f"MFA Policy ({self.policy_key})"
