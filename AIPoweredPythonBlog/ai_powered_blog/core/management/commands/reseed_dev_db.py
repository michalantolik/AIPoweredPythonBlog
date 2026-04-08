import os
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Reset DEV database (delete DB, migrate, seed)."

    def handle(self, *args, **options):
        # 🚨 Safety check
        if not settings.DEBUG:
            raise CommandError("reset_dev_db can only run in DEBUG mode!")

        db_settings = settings.DATABASES["default"]
        engine = db_settings["ENGINE"]

        self.stdout.write(self.style.WARNING("Resetting DEV database..."))

        # 🧹 SQLITE (your case)
        if "sqlite3" in engine:
            db_path = db_settings["NAME"]

            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(f"Deleted SQLite DB: {db_path}")
            else:
                self.stdout.write("SQLite DB does not exist, skipping delete.")

        # 🧹 POSTGRES / OTHERS (optional basic support)
        else:
            raise CommandError(
                "reset_dev_db currently supports only SQLite. Extend if needed."
            )

        # 🔄 Migrate
        self.stdout.write("Running migrations...")
        call_command("migrate")

        # 🌱 Seed
        self.stdout.write("Seeding database...")
        call_command("seed_db")

        self.stdout.write(self.style.SUCCESS("DEV database reset complete."))