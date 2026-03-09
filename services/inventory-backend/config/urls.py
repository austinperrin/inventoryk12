"""
URL configuration for config project.
"""

from django.conf import settings
from django.urls import include, path


def build_api_prefix(app_env_path_prefix: str) -> str:
    env_prefix = app_env_path_prefix.strip("/")
    return f"{env_prefix}/api/v1" if env_prefix else "api/v1"


api_prefix = build_api_prefix(settings.APP_ENV_PATH_PREFIX)

urlpatterns: list[object] = [
    path(f"{api_prefix}/auth/", include("apps.identity.api.v1.urls")),
    path(f"{api_prefix}/common/", include("apps.common.api.v1.urls")),
]
