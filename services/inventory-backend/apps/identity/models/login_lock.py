from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.utils import timezone
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class UserLoginLock(BaseModel, AuditModel):
    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="login_locks",
    )
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_user_login_lock",
    )

    class Meta:
        db_table = "identity_user_login_lock"
        verbose_name = "User Login Lock"
        verbose_name_plural = "User Login Locks"
        indexes = [
            models.Index(fields=["user", "starts_at", "ends_at"], name="id_usr_lock_usr_win_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(ends_at__isnull=True) | Q(ends_at__gte=models.F("starts_at")),
                name="id_usr_lock_win_chk",
            )
        ]


class RoleLoginLock(BaseModel, AuditModel):
    role = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="identity_role_login_locks",
    )
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_identity_role_login_lock",
    )

    class Meta:
        db_table = "identity_role_login_lock"
        verbose_name = "Role Login Lock"
        verbose_name_plural = "Role Login Locks"
        indexes = [
            models.Index(fields=["role", "starts_at", "ends_at"], name="id_role_lock_role_win_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(ends_at__isnull=True) | Q(ends_at__gte=models.F("starts_at")),
                name="id_role_lock_win_chk",
            )
        ]
