"""
URL configuration for config project.
"""

from django.urls import include, path

urlpatterns: list[object] = [
    path("api/v1/common/", include("apps.common.api.v1.urls")),
    path("api/v1/auth/", include("apps.identity.api.v1.urls")),
    path("api/v1/organization/", include("apps.organization.api.v1.urls")),
    path("api/v1/academic/", include("apps.academic.api.v1.urls")),
    path("api/v1/instruction/", include("apps.instruction.api.v1.urls")),
    path("api/v1/enrollment/", include("apps.enrollment.api.v1.urls")),
    path("api/v1/contacts/", include("apps.contacts.api.v1.urls")),
    path("api/v1/inventory/", include("apps.inventory.api.v1.urls")),
    path("api/v1/operations/", include("apps.operations.api.v1.urls")),
    path("api/v1/integrations/", include("apps.integrations.api.v1.urls")),
]
