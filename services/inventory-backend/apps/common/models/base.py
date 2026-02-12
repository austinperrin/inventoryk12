import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base class with UUID primary key and audit-friendly timestamps.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
