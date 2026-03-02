import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base class with internal integer PK, external UUID, and timestamps.
    """

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
