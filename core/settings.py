import os
from pathlib import Path
from datetime import timedelta
import environ

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Applications
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

    # Local apps
    "app.users",
    "app.webhooks",
    "app.events",
    "app.deliveries",
]

# Custom User Model
AUTH_USER_MODEL = "users.User"

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# URLs
ROOT_URLCONF = "core.urls"

# Templates
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

# Database (Render PostgreSQL via DATABASE_URL)
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Celery (Redis from Render)
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
