# ======================================================================
# DEVELOPMENT SETTINGS
# Local development configuration. Extends base.py with development-only
# behavior such as debugging, browsable API support, and relaxed options.
# ======================================================================

from datetime import timedelta

from . import base as base_settings

BASE_DIR = base_settings.BASE_DIR
REPO_ROOT = base_settings.REPO_ROOT
env = base_settings.env
SECRET_KEY = base_settings.SECRET_KEY
DEBUG = base_settings.DEBUG
ALLOWED_HOSTS = base_settings.ALLOWED_HOSTS
INSTALLED_APPS = base_settings.INSTALLED_APPS
MIDDLEWARE = base_settings.MIDDLEWARE
ROOT_URLCONF = base_settings.ROOT_URLCONF
WSGI_APPLICATION = base_settings.WSGI_APPLICATION
ASGI_APPLICATION = base_settings.ASGI_APPLICATION
TEMPLATES = base_settings.TEMPLATES
DATABASES = base_settings.DATABASES
AUTH_PASSWORD_VALIDATORS = base_settings.AUTH_PASSWORD_VALIDATORS
AUTH_USER_MODEL = base_settings.AUTH_USER_MODEL
LANGUAGE_CODE = base_settings.LANGUAGE_CODE
TIME_ZONE = base_settings.TIME_ZONE
USE_I18N = base_settings.USE_I18N
USE_TZ = base_settings.USE_TZ
REST_FRAMEWORK = base_settings.REST_FRAMEWORK
STATIC_URL = base_settings.STATIC_URL
STATIC_ROOT = base_settings.STATIC_ROOT
MEDIA_URL = base_settings.MEDIA_URL
MEDIA_ROOT = base_settings.MEDIA_ROOT
DEFAULT_AUTO_FIELD = base_settings.DEFAULT_AUTO_FIELD

# ----------------------------------------------------------------------
# SECURITY AND DEBUG
# ----------------------------------------------------------------------
DEBUG = True

# Open in development for convenience. Do not reuse in production.
ALLOWED_HOSTS = ["*"]

# ----------------------------------------------------------------------
# DJANGO REST FRAMEWORK (development overrides)
# ----------------------------------------------------------------------
# Enable browsable API for local development.
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = list(REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"])
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append("rest_framework.renderers.BrowsableAPIRenderer")

# Enable JWT authentication in development.
REST_FRAMEWORK.setdefault("DEFAULT_AUTHENTICATION_CLASSES", [])
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = list(
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
)
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
    "rest_framework_simplejwt.authentication.JWTAuthentication"
)

# Relaxed default permissions in development. Override as needed.
REST_FRAMEWORK.setdefault("DEFAULT_PERMISSION_CLASSES", [])
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = list(REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"])
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"].append(
    "rest_framework.permissions.IsAuthenticatedOrReadOnly"
)

# ----------------------------------------------------------------------
# SIMPLE JWT (development lifetimes)
# ----------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ----------------------------------------------------------------------
# EMAIL
# ----------------------------------------------------------------------
# Print emails to the console during development.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ----------------------------------------------------------------------
# CORS (for frontend dev server such as Vite)
# ----------------------------------------------------------------------
# If your frontend runs on a separate dev server (e.g., Vite),
# uncomment this section as needed.
#
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
#
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# ----------------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------------
# Basic logging for development. Production logging is defined in prod.py.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
