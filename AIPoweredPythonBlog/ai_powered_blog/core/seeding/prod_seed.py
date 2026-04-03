from django.conf import settings
from django.core.management.base import CommandError
from django.utils.text import slugify

from tags.models import Tag
from users.models import User


def run_prod_seed(stdout, style):
    stdout.write("Seeding production superuser...")
    _seed_prod_superuser(stdout, style)

    stdout.write("Seeding tags...")
    _seed_tags(stdout, style)

    stdout.write("Production seed mode skips demo users, demo posts, and demo comments.")


def _seed_prod_superuser(stdout, style):
    username = getattr(settings, "SEED_SUPERUSER_USERNAME", "").strip()
    email = getattr(settings, "SEED_SUPERUSER_EMAIL", "").strip()
    password = getattr(settings, "SEED_SUPERUSER_PASSWORD", "")

    if not username:
        raise CommandError("DJANGO_SUPERUSER_USERNAME is required for prod seed mode.")
    if not email:
        raise CommandError("DJANGO_SUPERUSER_EMAIL is required for prod seed mode.")
    if not password:
        raise CommandError("DJANGO_SUPERUSER_PASSWORD is required for prod seed mode.")

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


def _seed_tags(stdout, style):
    tag_names = [
        "python",
        "django",
        "architecture",
        "backend",
        "testing",
        "api",
        "clean-code",
        "database",
    ]

    tags = []

    for name in tag_names:
        slug = slugify(name)
        tag, created = Tag.objects.get_or_create(
            slug=slug,
            defaults={"name": name},
        )

        if tag.name != name:
            tag.name = name
            tag.save()

        if created:
            stdout.write(style.SUCCESS(f"Created tag: {tag.name}"))
        else:
            stdout.write(f"Tag already exists: {tag.name}")

        tags.append(tag)

    return tags
