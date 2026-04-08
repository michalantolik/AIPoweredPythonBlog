from django.contrib.auth import get_user_model
from django.db import transaction


def seed():
    """
    Base seeding.
    Keep only things that are safe for ALL environments.
    """
    with transaction.atomic():
        create_base_superuser()


def create_base_superuser():
    """
    Optional shared admin creation.
    You can remove this if you do not want it in all environments.
    """
    user = get_user_model()

    username = "admin"
    email = "admin@example.com"
    password = "change-me-now"

    if not user.objects.filter(username=username).exists():
        user.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
