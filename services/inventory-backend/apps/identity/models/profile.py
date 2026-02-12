from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Profile(BaseModel):
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
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    display_name = models.CharField(max_length=150, blank=True)

    # Contact + locale details (separate from auth email)
    phone_number = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=100, default="UTC")

    class Meta:
        db_table = "identity_profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        if self.display_name:
            return self.display_name
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return f"Profile for {self.user.email}"
