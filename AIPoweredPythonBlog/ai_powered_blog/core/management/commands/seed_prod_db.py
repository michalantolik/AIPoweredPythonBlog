import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Seed PROD database with minimal required data only."

    def handle(self, *args, **options):
        if settings.DEBUG:
            raise CommandError("seed_db cannot run when DEBUG=True.")

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        missing_vars = [
            name
            for name, value in {
                "DJANGO_SUPERUSER_USERNAME": username,
                "DJANGO_SUPERUSER_EMAIL": email,
                "DJANGO_SUPERUSER_PASSWORD": password,
            }.items()
            if not value
        ]

        if missing_vars:
            raise CommandError(
                "Missing required environment variables for PROD seeding: "
                + ", ".join(missing_vars)
            )

        self.stdout.write("Seeding PROD database...")

        with transaction.atomic():
            user_model = get_user_model()

            admin_user, created = user_model.objects.update_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            admin_user.set_password(password)
            admin_user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"PROD superuser '{username}' created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"PROD superuser '{username}' updated successfully.")
            )

        self.stdout.write(self.style.SUCCESS("PROD database seeding complete."))
