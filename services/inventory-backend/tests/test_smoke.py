import django
from django.conf import settings
from django.test import Client


def test_django_settings_load() -> None:
    django.setup()


def test_common_health_endpoint_returns_ok() -> None:
    client = Client()

    response = client.get(f"{settings.APP_ENV_PATH_PREFIX}/api/v1/common/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
