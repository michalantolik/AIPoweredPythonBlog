from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.seeding.dev_seed import run_dev_seed
from core.seeding.prod_seed import run_prod_seed


class Command(BaseCommand):
    help = "Seed database in dev or prod mode"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            choices=["auto", "dev", "prod"],
            default="auto",
            help="Seed mode. Use 'auto' to resolve from DJANGO_SEED_MODE / DJANGO_ENV.",
        )

    def handle(self, *args, **options):
        mode = self._resolve_mode(options["mode"])

        self.stdout.write(self.style.WARNING(f"Starting seed in '{mode}' mode..."))

        with transaction.atomic():
            if mode == "dev":
                run_dev_seed(self.stdout, self.style)
            elif mode == "prod":
                run_prod_seed(self.stdout, self.style)
            else:
                raise CommandError(f"Unsupported seed mode: {mode}")

        self.stdout.write(self.style.SUCCESS(f"Seeding finished successfully in '{mode}' mode."))

    def _resolve_mode(self, requested_mode: str) -> str:
        if requested_mode != "auto":
            return requested_mode

        mode_from_settings = getattr(settings, "DEFAULT_SEED_MODE", "").strip().lower()
        if mode_from_settings in {"dev", "prod"}:
            return mode_from_settings

        environment = getattr(settings, "ENVIRONMENT", "dev").strip().lower()
        return "prod" if environment == "prod" else "dev"
