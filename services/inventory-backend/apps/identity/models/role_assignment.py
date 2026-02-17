from datetime import date

from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class RoleAssignment(BaseModel, AuditModel):
    """
    Time-windowed role assignment for a user.

    Organization scope is handled through related RoleAssignmentOrganization rows.
    """

    user = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="role_assignments",
    )
    role = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="identity_role_assignments",
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(excluded_fields=["created_at", "updated_at"])

    class Meta:
        db_table = "identity_role_assignment"
        verbose_name = "Role Assignment"
        verbose_name_plural = "Role Assignments"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="identity_role_assignment_valid_date_window",
            )
        ]

    def is_active_on(self, on_date: date) -> bool:
        if self.starts_on > on_date:
            return False
        if self.ends_on is not None and self.ends_on < on_date:
            return False
        return True


class RoleAssignmentOrganization(BaseModel, AuditModel):
    """
    Organization scope rows for role assignments.

    Links role assignment scope to organization rows.
    """

    role_assignment = models.ForeignKey(
        "identity.RoleAssignment",
        on_delete=models.CASCADE,
        related_name="organization_scopes",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="role_assignment_scopes",
    )
    history = HistoricalRecords(excluded_fields=["created_at", "updated_at"])

    class Meta:
        db_table = "identity_role_assignment_organization"
        verbose_name = "Role Assignment Organization"
        verbose_name_plural = "Role Assignment Organizations"
        constraints = [
            models.UniqueConstraint(
                fields=["role_assignment", "organization"],
                name="identity_role_assignment_org_unique",
            )
        ]
