import django


def test_django_settings_load() -> None:
    django.setup()
