import importlib

from django.conf import settings
from django.test import Client, override_settings
from django.urls import clear_url_caches, set_urlconf

import config.urls as project_urls


def _reload_urls_with_env_prefix(path_prefix: str) -> None:
    with override_settings(APP_ENV_PATH_PREFIX=path_prefix):
        importlib.reload(project_urls)
        clear_url_caches()
        set_urlconf("config.urls")


def _restore_default_urlconf() -> None:
    importlib.reload(project_urls)
    clear_url_caches()
    set_urlconf(None)


def test_build_api_prefix_supports_prod_and_non_prod_paths() -> None:
    assert project_urls.build_api_prefix("/prod") == "prod/api/v1"
    assert project_urls.build_api_prefix("/sandbox") == "sandbox/api/v1"
    assert project_urls.build_api_prefix("/") == "api/v1"


def test_common_health_endpoint_routes_under_prod_prefix() -> None:
    _reload_urls_with_env_prefix("/prod")
    client = Client()
    try:
        response = client.get("/prod/api/v1/common/health/")
    finally:
        _restore_default_urlconf()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_common_health_endpoint_routes_under_non_prod_prefix() -> None:
    _reload_urls_with_env_prefix("/sandbox")
    client = Client()
    try:
        response = client.get("/sandbox/api/v1/common/health/")
    finally:
        _restore_default_urlconf()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unconfigured_environment_path_returns_404_for_current_env_prefix() -> None:
    client = Client()

    response = client.get(f"{settings.APP_ENV_PATH_PREFIX}/api/v1/common/health/")
    wrong_env_response = client.get("/prod/api/v1/common/health/")

    assert response.status_code == 200
    assert wrong_env_response.status_code == 404
