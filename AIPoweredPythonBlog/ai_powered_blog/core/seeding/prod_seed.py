import os

from django.conf import settings
from django.core.management.base import CommandError

from core.seeding.dev_seed import run_dev_seed
from users.models import User


def run_prod_seed(stdout, style):
    stdout.write("Seeding production superuser...")
    _seed_prod_superuser(stdout, style)

    stdout.write("Seeding production database with the same content as dev...")
    run_dev_seed(stdout, style)

    stdout.write(style.SUCCESS("Production seed completed with dev-equivalent content."))


def _seed_prod_superuser(stdout, style):
    username = (
        os.getenv("SEED_SUPERUSER_USERNAME")
        or getattr(settings, "SEED_SUPERUSER_USERNAME", "")
    ).strip()

    email = (
        os.getenv("SEED_SUPERUSER_EMAIL")
        or getattr(settings, "SEED_SUPERUSER_EMAIL", "")
    ).strip()

    password = (
        os.getenv("SEED_SUPERUSER_PASSWORD")
        or getattr(settings, "SEED_SUPERUSER_PASSWORD", "")
    )

    if not username:
        raise CommandError("SEED_SUPERUSER_USERNAME is required for prod seed mode.")
    if not email:
        raise CommandError("SEED_SUPERUSER_EMAIL is required for prod seed mode.")
    if not password:
        raise CommandError("SEED_SUPERUSER_PASSWORD is required for prod seed mode.")

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
        },
    )

    updated = False

    if user.email != email:
        user.email = email
        updated = True

    if not user.is_staff:
        user.is_staff = True
        updated = True

    if not user.is_superuser:
        user.is_superuser = True
        updated = True

    user.set_password(password)
    updated = True

    if created or updated:
        user.save()

    if created:
        stdout.write(style.SUCCESS(f"Created production superuser: {user.username}"))
    else:
        stdout.write(f"Production superuser is ready: {user.username}")

    return user
