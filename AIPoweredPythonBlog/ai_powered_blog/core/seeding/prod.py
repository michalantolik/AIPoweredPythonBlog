from django.contrib.auth import get_user_model
from django.db import transaction


def seed():
    """
    PROD seeding.
    Keep this minimal and safe.
    Only required data.
    """
    with transaction.atomic():
        create_prod_superuser()


def create_prod_superuser():
    """
    Example only.
    Best practice: read values from env vars.
    Skip creation if values are missing.
    """
    from django.conf import settings

    user = get_user_model()

    # You can later move these to dedicated env helpers if you want.
    import os
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not username or not email or not password:
        return

    if not user.objects.filter(username=username).exists():
        user.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
