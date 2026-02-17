from datetime import date
from typing import Any, ClassVar

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
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

        email = self.normalize_email(email)
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
        excluded_fields=["password", "last_login", "created_at", "updated_at"]
    )

    # Authentication configuration
    USERNAME_FIELD: ClassVar[str] = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []  # no secondary login fields

    class Meta:
        db_table = "identity_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["created_at"]  # comes from BaseModel

    def __str__(self) -> str:
        return self.email

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
