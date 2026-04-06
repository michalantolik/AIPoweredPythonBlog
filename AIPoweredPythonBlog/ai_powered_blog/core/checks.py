from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


DEFAULT_INSECURE_SECRET_KEY = (
    "django-insecure-xoj4nsk4w@+^4&3v6%$jeu3b(iior(4(&wbp25m2oibat#3_q+"
)


@register(Tags.security, deploy=True)
def production_security_checks(app_configs, **kwargs):
    messages = []

    if getattr(settings, "DEBUG", False):
        return messages

    secret_key = getattr(settings, "SECRET_KEY", "")
    allowed_hosts = list(getattr(settings, "ALLOWED_HOSTS", []))

    if not secret_key or secret_key == DEFAULT_INSECURE_SECRET_KEY:
        messages.append(
            Error(
                "Production SECRET_KEY must be explicitly configured and must not use the repository default.",
                hint="Set DJANGO_SECRET_KEY to a long random secret from your environment or secret manager.",
                id="core.E001",
            )
        )

    if "*" in allowed_hosts:
        messages.append(
            Error(
                'ALLOWED_HOSTS cannot contain "*" in production.',
                hint="Set DJANGO_ALLOWED_HOSTS to explicit host names only.",
                id="core.E002",
            )
        )

    if getattr(settings, "SECURE_HSTS_SECONDS", 0) <= 0:
        messages.append(
            Warning(
                "HSTS is not enabled in production.",
                hint="Set DJANGO_SECURE_HSTS_SECONDS to a small test value first, then increase it after HTTPS verification.",
                id="core.W001",
            )
        )

    return messages
