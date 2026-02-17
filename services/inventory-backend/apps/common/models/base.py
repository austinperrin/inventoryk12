import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base class with internal integer PK, external UUID, and timestamps.
    """

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
