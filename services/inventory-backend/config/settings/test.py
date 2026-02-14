# ======================================================================
# TEST SETTINGS
# Fast, isolated configuration for automated test runs.
# ======================================================================

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

# ----------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# ----------------------------------------------------------------------
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [  # noqa: F405
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]
