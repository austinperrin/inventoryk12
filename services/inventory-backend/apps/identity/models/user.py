from datetime import date, datetime
from typing import Any, ClassVar

from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class UserManager(BaseUserManager["User"]):
    """
    Custom manager for email-based user accounts.
    Provides helpers for standard users and superusers.
    """

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "User":
        if not email:
            raise ValueError("Email is required for user accounts.")

        email = self.normalize_email(email).strip().lower()
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AuditModel, AbstractBaseUser, PermissionsMixin):
    """
    Primary user model for authentication and system identity.
    Inherits BaseModel for integer IDs, external UUID, and timestamps.
    Designed to stay minimal while remaining IAM-ready.
    """

    # Primary identity fields
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Account status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    require_password_reset = models.BooleanField(default=False)

    # User lifecycle
    activated_at = models.DateTimeField(null=True, blank=True)
    inactivated_at = models.DateTimeField(null=True, blank=True)
    inactivated_by = models.ForeignKey(
        "identity.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inactivated_user_set",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Timestamp when the user was first verified "
            "(successful auth or administrative verification)."
        ),
    )

    # Manager
    objects: ClassVar[UserManager] = UserManager()
    history = HistoricalRecords(
        excluded_fields=["password", "last_login", "created_at", "updated_at"],
        table_name="hist_identity_user",
    )

    # Authentication configuration
    USERNAME_FIELD: ClassVar[str] = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []  # no secondary login fields

    class Meta:
        db_table = "identity_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["created_at"]  # comes from BaseModel
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="identity_user_email_ci_unique",
            )
        ]
        indexes = [
            models.Index(fields=["is_active", "is_staff"], name="identity_user_active_staff_idx"),
            models.Index(fields=["inactivated_at"], name="id_user_inact_at_idx"),
        ]

    def __str__(self) -> str:
        return self.email

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def has_active_role_assignment(self, on_date: date | None = None) -> bool:
        check_date = on_date or date.today()
        return self.role_assignments.filter(
            starts_on__lte=check_date,
        ).filter(models.Q(ends_on__isnull=True) | models.Q(ends_on__gte=check_date)).exists()

    def active_role_names(self, on_date: date | None = None) -> list[str]:
        check_date = on_date or date.today()
        return sorted(
            self.role_assignments.filter(starts_on__lte=check_date)
            .filter(models.Q(ends_on__isnull=True) | models.Q(ends_on__gte=check_date))
            .values_list("role__name", flat=True)
            .distinct()
        )

    def has_active_user_login_lock(self, at_time: datetime | None = None) -> bool:
        check_time = at_time or timezone.now()
        return self.login_locks.filter(starts_at__lte=check_time).filter(
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=check_time)
        ).exists()

    def has_active_role_login_lock(self, at_time: datetime | None = None) -> bool:
        check_time = at_time or timezone.now()
        check_date = check_time.date()

        active_role_ids = list(
            self.role_assignments.filter(starts_on__lte=check_date)
            .filter(models.Q(ends_on__isnull=True) | models.Q(ends_on__gte=check_date))
            .values_list("role_id", flat=True)
            .distinct()
        )
        if not active_role_ids:
            return False

        role_lock_model = apps.get_model("identity", "RoleLoginLock")
        role_lock_qs = role_lock_model.objects.filter(
            role_id__in=active_role_ids,
            starts_at__lte=check_time,
        ).filter(models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=check_time))
        return role_lock_qs.exists()

    def can_authenticate(self, at_time: datetime | None = None) -> bool:
        check_time = at_time or timezone.now()
        return (
            self.is_active
            and self.has_active_role_assignment(check_time.date())
            and not self.has_active_user_login_lock(check_time)
            and not self.has_active_role_login_lock(check_time)
        )
