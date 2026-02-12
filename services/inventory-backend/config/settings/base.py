# ======================================================================
# BASE SETTINGS
# Core settings shared across all environments. Environment-specific
# overrides should be defined in dev.py, test.py, and prod.py.
# ======================================================================

from pathlib import Path
from typing import Any

import environ

# ----------------------------------------------------------------------
# PATHS
# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(BASE_DIR)
REPO_ROOT = BASE_DIR.parent
# print(REPO_ROOT)

# ----------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# ----------------------------------------------------------------------
env = environ.Env()

# Read root-level env file if present; safe to skip in production.
env_file = REPO_ROOT / ".env.backend"
if env_file.exists():
    env.read_env(env_file)
else:
    fallback_env_file = REPO_ROOT / "configs" / "env" / ".env.backend"
    if fallback_env_file.exists():
        env.read_env(fallback_env_file)

# ----------------------------------------------------------------------
# SECURITY AND CORE CONFIGURATION
# ----------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
# This fallback is intentionally insecure for development only.
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-development-key-not-for-production",
)

# DEBUG mode should always be overridden by environment-specific settings.
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# ALLOWED_HOSTS should be explicitly set in each environment.
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# ----------------------------------------------------------------------
# APPLICATIONS
# ----------------------------------------------------------------------
INSTALLED_APPS = [
    # Apps that must run before Django's core apps
    # Django core apps
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # Project apps
    "apps.common",
    "apps.identity",
    "apps.inventory",
    "apps.districts",
]

# Custom user model
AUTH_USER_MODEL = "identity.User"

# ----------------------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------------------
MIDDLEWARE = [
    # Middleware that must run before standard Django middleware
    "corsheaders.middleware.CorsMiddleware",
    # Standard Django middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third-party middleware
    # Project middleware
]

# ----------------------------------------------------------------------
# URLS / WSGI / ASGI
# ----------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ----------------------------------------------------------------------
# TEMPLATES
# ----------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------------
# In dev: falls back to SQLite (safe default).
# In prod: DATABASE_URL should be set via environment.
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# ----------------------------------------------------------------------
# PASSWORD VALIDATION
# ----------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation.UserAttributeSimilarityValidator"),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ----------------------------------------------------------------------
# INTERNATIONALIZATION
# ----------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# ----------------------------------------------------------------------
# Base API behavior for all environments. Defaults keep the API
# stateless, predictable, and secure for multi-service communication.
REST_FRAMEWORK: dict[str, Any] = {
    # Renderers: JSON-only by default
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Parsers: JSON-only by default
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    # Authentication: leave undefined in base so environments can decide.
    # "DEFAULT_AUTHENTICATION_CLASSES": [],
    # Permissions: require explicit configuration in each environment.
    # "DEFAULT_PERMISSION_CLASSES": [],
    # Versioning: included early for multi-service integration.
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
}

# ----------------------------------------------------------------------
# STATIC AND MEDIA FILES
# ----------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ----------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
