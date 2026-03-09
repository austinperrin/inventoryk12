# ======================================================================
# TEST SETTINGS
# Fast, isolated configuration for automated test runs.
# ======================================================================

from . import base as base_settings
from .base import *  # noqa: F403

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
APP_ENV_PATH_PREFIX = base_settings.APP_ENV_PATH_PREFIX
AUTH_COOKIE_DOMAIN = base_settings.AUTH_COOKIE_DOMAIN
AUTH_COOKIE_PATH = base_settings.AUTH_COOKIE_PATH
AUTH_COOKIE_SAMESITE = base_settings.AUTH_COOKIE_SAMESITE
AUTH_COOKIE_SECURE = False
AUTH_ACCESS_COOKIE_MAX_AGE = base_settings.AUTH_ACCESS_COOKIE_MAX_AGE
AUTH_REFRESH_COOKIE_MAX_AGE = base_settings.AUTH_REFRESH_COOKIE_MAX_AGE
AUTH_SESSION_IDLE_TIMEOUT_SECONDS = base_settings.AUTH_SESSION_IDLE_TIMEOUT_SECONDS
AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS = base_settings.AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS
AUTH_REAUTH_COOKIE_NAME = base_settings.AUTH_REAUTH_COOKIE_NAME
AUTH_REAUTH_WINDOW_SECONDS = base_settings.AUTH_REAUTH_WINDOW_SECONDS
AUTH_REAUTH_COOKIE_SALT = base_settings.AUTH_REAUTH_COOKIE_SALT
AUTH_MFA_COOKIE_NAME = base_settings.AUTH_MFA_COOKIE_NAME
AUTH_MFA_RECENT_WINDOW_SECONDS = base_settings.AUTH_MFA_RECENT_WINDOW_SECONDS
AUTH_MFA_COOKIE_SALT = base_settings.AUTH_MFA_COOKIE_SALT
AUTH_MFA_CHALLENGE_TTL_SECONDS = base_settings.AUTH_MFA_CHALLENGE_TTL_SECONDS
SIMPLE_JWT = base_settings.SIMPLE_JWT
