"""
URL configuration for config project.
"""

from django.urls import include, path

urlpatterns: list[object] = [
    path("api/v1/common/", include("apps.common.api.v1.urls")),
    path("api/v1/auth/", include("apps.identity.api.v1.urls")),
    path("api/v1/inventory/", include("apps.inventory.api.v1.urls")),
    path("api/v1/districts/", include("apps.districts.api.v1.urls")),
]
