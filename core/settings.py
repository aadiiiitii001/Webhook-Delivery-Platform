import os
from pathlib import Path
from datetime import timedelta
import environ

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Env setup
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# APPLICATIONS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "django_filters",
    "corsheaders",

    # Local
    "app.users",
    "app.webhooks",
    "app.events",
    "app.deliveries",
]

# CUSTOM USER
AUTH_USER_MODEL = "users.User"

# MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be high
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# CORS (fix your unused dependency)
CORS_ALLOW_ALL_ORIGINS = True  # lock this down later

# URLS
ROOT_URLCONF = "core.urls"

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

# WSGI
WSGI_APPLICATION = "core.wsgi.application"

# DATABASE
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# CELERY
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# STATIC
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# DEFAULT FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
