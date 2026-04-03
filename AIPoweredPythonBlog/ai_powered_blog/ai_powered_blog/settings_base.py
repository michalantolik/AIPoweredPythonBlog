import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(name: str, default=None):
    return os.getenv(name, default)


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_list_env(name: str, default=None):
    raw_value = os.getenv(name)

    if raw_value is None or raw_value.strip() == "":
        return default or []

    return [item.strip() for item in raw_value.split(",") if item.strip()]


SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    "django-insecure-xoj4nsk4w@+^4&3v6%$jeu3b(iior(4(&wbp25m2oibat#3_q+",
)

DEBUG = get_bool_env("DJANGO_DEBUG", False)

ALLOWED_HOSTS = get_list_env(
    "DJANGO_ALLOWED_HOSTS",
    ["127.0.0.1", "localhost"],
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "comments",
    "core",
    "posts",
    "tags",
    "users",
    "website",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ai_powered_blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_ui_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "ai_powered_blog.wsgi.application"
ASGI_APPLICATION = "ai_powered_blog.asgi.application"

DATABASE_ENGINE = get_env("DJANGO_DB_ENGINE", "django.db.backends.sqlite3")

if DATABASE_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / get_env("DJANGO_SQLITE_NAME", "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "NAME": get_env("DJANGO_DB_NAME", ""),
            "USER": get_env("DJANGO_DB_USER", ""),
            "PASSWORD": get_env("DJANGO_DB_PASSWORD", ""),
            "HOST": get_env("DJANGO_DB_HOST", "localhost"),
            "PORT": get_env("DJANGO_DB_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

LANGUAGE_CODE = "en-us"
TIME_ZONE = get_env("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTRO_OVERLAY_ENABLED = get_bool_env("INTRO_OVERLAY_ENABLED", True)
INTRO_OVERLAY_DURATION_MS = int(get_env("INTRO_OVERLAY_DURATION_MS", "3600"))
INTRO_OVERLAY_IMAGE = get_env(
    "INTRO_OVERLAY_IMAGE",
    "images/intro/michal-portrait.png",
)

SHOW_SIDEBAR_ON_HOME_STARTUP = get_bool_env(
    "SHOW_SIDEBAR_ON_HOME_STARTUP",
    True,
)
