import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from posts.models import Category, Post
from tags.models import Tag


class Command(BaseCommand):
    help = "Reset DEV database (delete DB, migrate, seed DEV data)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("reseed_dev_db can only run when DEBUG=True.")

        db_settings = settings.DATABASES["default"]
        engine = db_settings["ENGINE"]

        self.stdout.write(self.style.WARNING("Resetting DEV database..."))

        if "sqlite3" not in engine:
            raise CommandError(
                "reseed_dev_db currently supports only SQLite. "
                "This command is intended for local DEV usage."
            )

        db_path = os.path.abspath(str(db_settings["NAME"]))

        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(f"Deleted SQLite DB: {db_path}")
        else:
            self.stdout.write("SQLite DB does not exist, skipping delete.")

        self.stdout.write("Running migrations...")
        call_command("migrate")

        self.stdout.write("\n---------------------------------------------\n")
        self.stdout.write("DEV database seeding [STARTED]")

        self._seed_dev_data()

        self.stdout.write("DEV database seeding [COMPLETED]")
        self.stdout.write("---------------------------------------------\n\n")

    def _seed_dev_data(self):
        with transaction.atomic():
            user_model = get_user_model()

            python_tag, _ = Tag.objects.update_or_create(
                slug="python",
                defaults={"name": "python"},
            )

            django_tag, _ = Tag.objects.update_or_create(
                slug="django",
                defaults={"name": "django"},
            )

            backend_category, _ = Category.objects.update_or_create(
                slug="backend",
                defaults={
                    "name": "Backend",
                    "sort_order": 1,
                },
            )

            author, _ = user_model.objects.update_or_create(
                username="devadmin",
                defaults={
                    "email": "devadmin@example.com",
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            author.set_password("devpassword123")
            author.save()

            posts_to_seed = [
                {
                    "slug": "dev-seed-post-1",
                    "title": "DEV Seed Post (1)",
                    "excerpt": "This post exists only in DEV seed (1).",
                    "content": "DEV seeded content (1).",
                },
                {
                    "slug": "dev-seed-post-2",
                    "title": "DEV Seed Post (2)",
                    "excerpt": "This post exists only in DEV seed (2).",
                    "content": "DEV seeded content (2).",
                },
                {
                    "slug": "dev-seed-post-3",
                    "title": "DEV Seed Post (3)",
                    "excerpt": "This post exists only in DEV seed (3).",
                    "content": "DEV seeded content (3).",
                },
                {
                    "slug": "dev-seed-post-4",
                    "title": "DEV Seed Post (4)",
                    "excerpt": "This post exists only in DEV seed (4).",
                    "content": "DEV seeded content (4).",
                },
                {
                    "slug": "dev-seed-post-5",
                    "title": "DEV Seed Post (5)",
                    "excerpt": "This post exists only in DEV seed (5).",
                    "content": "DEV seeded content (5).",
                },
            ]

            for item in posts_to_seed:
                post, _ = Post.objects.update_or_create(
                    slug=item["slug"],
                    defaults={
                        "title": item["title"],
                        "excerpt": item["excerpt"],
                        "content": item["content"],
                        "category": backend_category,
                        "author": author,
                        "published_at": timezone.now(),
                        "status": Post.Status.PUBLISHED,
                    },
                )
                post.tags.set([python_tag, django_tag])
