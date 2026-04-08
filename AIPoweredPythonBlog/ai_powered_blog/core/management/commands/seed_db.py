from importlib import import_module

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Run database seeding for the current Django settings module."

    def handle(self, *args, **options):
        seed_module_path = getattr(settings, "SEED_MODULE", None)

        if not seed_module_path:
            raise CommandError("SEED_MODULE is not configured.")

        self.stdout.write(f"Using seed module: {seed_module_path}")

        try:
            seed_module = import_module(seed_module_path)
        except Exception as exc:
            raise CommandError(
                f"Could not import seed module '{seed_module_path}': {exc}"
            ) from exc

        seed_func = getattr(seed_module, "seed", None)

        if seed_func is None:
            raise CommandError(
                f"Module '{seed_module_path}' does not contain seed() function."
            )

        seed_func()

        self.stdout.write(self.style.SUCCESS("Database seeding completed."))
