"""
URL configuration for config project.
"""

from django.conf import settings
from django.urls import include, path

env_prefix = settings.APP_ENV_PATH_PREFIX.strip("/")
api_prefix = f"{env_prefix}/api/v1" if env_prefix else "api/v1"

urlpatterns: list[object] = [
    path(f"{api_prefix}/auth/", include("apps.identity.api.v1.urls")),
    path(f"{api_prefix}/common/", include("apps.common.api.v1.urls")),
]
