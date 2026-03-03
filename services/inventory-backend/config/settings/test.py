# ======================================================================
# TEST SETTINGS
# Fast, isolated configuration for automated test runs.
# ======================================================================

from .base import *  # noqa: F403
from . import base as base_settings

# ----------------------------------------------------------------------
# SECURITY AND DEBUG
# ----------------------------------------------------------------------
DEBUG = False
ALLOWED_HOSTS = ["testserver"]

# ----------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# ----------------------------------------------------------------------
# PASSWORDS
# ----------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# ----------------------------------------------------------------------
# EMAIL
# ----------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

AUTH_ACCESS_COOKIE_NAME = base_settings.AUTH_ACCESS_COOKIE_NAME
AUTH_REFRESH_COOKIE_NAME = base_settings.AUTH_REFRESH_COOKIE_NAME
AUTH_COOKIE_DOMAIN = base_settings.AUTH_COOKIE_DOMAIN
AUTH_COOKIE_PATH = base_settings.AUTH_COOKIE_PATH
AUTH_COOKIE_SAMESITE = base_settings.AUTH_COOKIE_SAMESITE
AUTH_COOKIE_SECURE = False
AUTH_ACCESS_COOKIE_MAX_AGE = base_settings.AUTH_ACCESS_COOKIE_MAX_AGE
AUTH_REFRESH_COOKIE_MAX_AGE = base_settings.AUTH_REFRESH_COOKIE_MAX_AGE
SIMPLE_JWT = base_settings.SIMPLE_JWT
