import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_INSECURE_SECRET_KEY = (
    "django-insecure-xoj4nsk4w@+^4&3v6%$jeu3b(iior(4(&wbp25m2oibat#3_q+"
)


def get_env(name: str, default=None):
    return os.getenv(name, default)


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return int(value)


def get_list_env(name: str, default=None):
    raw_value = os.getenv(name)

    if raw_value is None or raw_value.strip() == "":
        return default or []

    return [item.strip() for item in raw_value.split(",") if item.strip()]


SECRET_KEY = get_env("DJANGO_SECRET_KEY", DEFAULT_INSECURE_SECRET_KEY)

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
    "api",
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
    "core.middleware.SecurityHeadersMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

db_secret = {}
db_secret_raw = get_env("DJANGO_DB_SECRET_JSON", "")

if db_secret_raw:
    try:
        db_secret = json.loads(db_secret_raw)
    except json.JSONDecodeError as exc:
        raise ValueError("DJANGO_DB_SECRET_JSON must contain valid JSON.") from exc

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
            "NAME": get_env("DJANGO_DB_NAME", db_secret.get("dbname", "")),
            "USER": get_env("DJANGO_DB_USER", db_secret.get("username", "")),
            "PASSWORD": get_env("DJANGO_DB_PASSWORD", db_secret.get("password", "")),
            "HOST": get_env("DJANGO_DB_HOST", db_secret.get("host", "localhost")),
            "PORT": get_env("DJANGO_DB_PORT", str(db_secret.get("port", "5432"))),
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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTRO_OVERLAY_ENABLED = get_bool_env("INTRO_OVERLAY_ENABLED", True)
INTRO_OVERLAY_DURATION_MS = get_int_env("INTRO_OVERLAY_DURATION_MS", 3600)
INTRO_OVERLAY_IMAGE = get_env(
    "INTRO_OVERLAY_IMAGE",
    "images/intro/michal-portrait.png",
)

SHOW_SIDEBAR_ON_HOME_STARTUP = get_bool_env(
    "SHOW_SIDEBAR_ON_HOME_STARTUP",
    True,
)

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = get_env("DJANGO_SESSION_COOKIE_SAMESITE", "Lax")

CSRF_COOKIE_HTTPONLY = get_bool_env("DJANGO_CSRF_COOKIE_HTTPONLY", True)
CSRF_COOKIE_SAMESITE = get_env("DJANGO_CSRF_COOKIE_SAMESITE", "Lax")

SECURE_REFERRER_POLICY = get_env(
    "DJANGO_SECURE_REFERRER_POLICY",
    "strict-origin-when-cross-origin",
)

SECURE_CROSS_ORIGIN_OPENER_POLICY = get_env(
    "DJANGO_SECURE_CROSS_ORIGIN_OPENER_POLICY",
    "same-origin",
)

APP_CSP_ENABLED = get_bool_env("DJANGO_APP_CSP_ENABLED", True)

APP_CSP_DIRECTIVES = {
    "default-src": ("'self'",),
    "script-src": ("'self'",),
    "style-src": ("'self'",),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "data:"),
    "connect-src": ("'self'",),
    "object-src": ("'none'",),
    "base-uri": ("'self'",),
    "frame-ancestors": ("'none'",),
    "form-action": ("'self'",),
}

APP_CSP_EXCLUDE_PATH_PREFIXES = ("/admin/",)

APP_PERMISSIONS_POLICY_ENABLED = get_bool_env(
    "DJANGO_PERMISSIONS_POLICY_ENABLED",
    True,
)

APP_PERMISSIONS_POLICY = {
    "accelerometer": (),
    "autoplay": (),
    "camera": (),
    "display-capture": (),
    "geolocation": (),
    "gyroscope": (),
    "microphone": (),
    "payment": (),
    "usb": (),
}
