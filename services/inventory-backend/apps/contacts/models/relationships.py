from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

from apps.common.models import AuditModel, BaseModel


class StudentRelationship(BaseModel, AuditModel):
    student = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="student_relationships",
    )
    related_student = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="related_student_relationships",
    )
    relationship_label = models.CharField(max_length=100, blank=True)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_student_relationship",
    )

    class Meta:
        db_table = "contacts_student_relationship"
        verbose_name = "Student Relationship"
        verbose_name_plural = "Student Relationships"
        constraints = [
            models.CheckConstraint(
                check=~Q(student=models.F("related_student")),
                name="ct_stu_rel_not_self",
            ),
            models.CheckConstraint(
                check=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ct_stu_rel_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["student", "related_student", "relationship_label"],
                name="ct_stu_rel_unique",
            ),
        ]


class StudentGuardianRelationship(BaseModel, AuditModel):
    student = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="guardian_links",
    )
    guardian = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="student_links",
    )
    relationship_label = models.CharField(max_length=100, blank=True)
    is_primary_contact = models.BooleanField(default=False)
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_student_guardian_relationship",
    )

    class Meta:
        db_table = "contacts_student_guardian_relationship"
        verbose_name = "Student Guardian Relationship"
        verbose_name_plural = "Student Guardian Relationships"
        constraints = [
            models.CheckConstraint(
                check=Q(ends_on__isnull=True)
                | Q(starts_on__isnull=True)
                | Q(ends_on__gte=models.F("starts_on")),
                name="ct_stu_guard_rel_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["student", "guardian"],
                name="ct_stu_guard_unique",
            ),
            models.UniqueConstraint(
                fields=["student"],
                condition=Q(is_primary_contact=True),
                name="ct_stu_guard_primary_unique",
            ),
        ]


class StaffAssignment(BaseModel, AuditModel):
    staff = models.ForeignKey(
        "identity.User",
        on_delete=models.CASCADE,
        related_name="staff_contact_assignments",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        related_name="staff_contact_assignments",
        null=True,
        blank=True,
    )
    facility = models.ForeignKey(
        "locations.Facility",
        on_delete=models.CASCADE,
        related_name="staff_contact_assignments",
        null=True,
        blank=True,
    )
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    history = HistoricalRecords(
        excluded_fields=["created_at", "updated_at"],
        table_name="hist_contacts_staff_assignment",
    )

    class Meta:
        db_table = "contacts_staff_assignment"
        verbose_name = "Staff Assignment"
        verbose_name_plural = "Staff Assignments"
        constraints = [
            models.CheckConstraint(
                check=Q(organization__isnull=False, facility__isnull=True)
                | Q(organization__isnull=True, facility__isnull=False),
                name="ct_staff_asgn_single_scope",
            ),
            models.CheckConstraint(
                check=Q(ends_on__isnull=True) | Q(ends_on__gte=models.F("starts_on")),
                name="ct_staff_asgn_valid_date_win",
            ),
            models.UniqueConstraint(
                fields=["staff", "organization", "facility", "starts_on"],
                name="ct_staff_asgn_unique_start",
            ),
        ]
