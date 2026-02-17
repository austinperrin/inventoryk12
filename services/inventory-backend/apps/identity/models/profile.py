from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class Profile(BaseModel, AuditModel):
    """
    User-facing profile data.

    Profile contains user-facing details that do not belong in the auth model.
    Keeping this separate keeps authentication lean while profile data evolves
    with product needs.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Profile identity details
    preferred_name = models.CharField(max_length=150, blank=True)
    display_name = models.CharField(max_length=150, blank=True)

    # Contact + locale details (separate from auth email)
    phone_number = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=100, default="UTC")
    history = HistoricalRecords(excluded_fields=["created_at", "updated_at"])

    class Meta:
        db_table = "identity_profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        if self.display_name:
            return self.display_name
        if self.preferred_name:
            return self.preferred_name
        return f"Profile for {self.user.email}"
