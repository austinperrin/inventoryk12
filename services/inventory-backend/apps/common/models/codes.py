from django.db import models

from .audit import AuditModel
from .base import BaseModel


class CodeTableModel(BaseModel, AuditModel):
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_system_managed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["sort_order", "code"]

    def __str__(self) -> str:
        return self.label or self.code
