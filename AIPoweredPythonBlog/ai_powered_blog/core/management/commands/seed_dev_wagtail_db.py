import json
import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from wagtail.models import Site

from cms.models import BlogIndexPage, BlogPostPage


class Command(BaseCommand):
    help = "Reset DEV database (delete DB, migrate, seed DEV Wagtail data)"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_dev_wagtail_db can only run when DEBUG=True")

        db_settings = settings.DATABASES["default"]
        engine = db_settings["ENGINE"]

        self.stdout.write(self.style.WARNING("Resetting DEV database for Wagtail seeding..."))

        if "sqlite3" not in engine:
            raise CommandError(
                "seed_dev_wagtail_db currently supports only SQLite. "
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
        self.stdout.write("DEV Wagtail database seeding [STARTED]")

        self._seed_dev_data()

        self.stdout.write("DEV Wagtail database seeding [COMPLETED]")
        self.stdout.write("---------------------------------------------\n\n")

    def _seed_dev_data(self):
        with transaction.atomic():
            user_model = get_user_model()
            seed_data = self._load_seed_data()

            users_by_username = {}
            for item in seed_data["users"]:
                password = item["password"]
                user_defaults = {
                    key: value
                    for key, value in item.items()
                    if key not in {"username", "password"}
                }

                user, _ = user_model.objects.update_or_create(
                    username=item["username"],
                    defaults=user_defaults,
                )
                user.set_password(password)
                user.save()
                users_by_username[user.username] = user

            call_command("bootstrap_wagtail_blog")
            blog_index = self._get_blog_index()

            for item in seed_data["wagtail_posts"]:
                author = self._get_required_reference(
                    mapping=users_by_username,
                    key=item["author_username"],
                    entity_name="author",
                    post_slug=item["slug"],
                )

                published_at = self._parse_published_at(item.get("published_at"))
                published_on = self._parse_published_on(
                    item.get("published_on"),
                    fallback_datetime=published_at,
                )
                body_value = self._build_streamfield_value(
                    raw_value=item.get("body", []),
                    post_slug=item["slug"],
                )

                page = BlogPostPage.objects.child_of(blog_index).filter(slug=item["slug"]).first()

                if page is None:
                    page = BlogPostPage(
                        title=item["title"],
                        slug=item["slug"],
                        excerpt=item.get("excerpt", ""),
                        topic=item.get("topic", ""),
                        body=body_value,
                        published_on=published_on,
                        owner=author,
                        show_in_menus=item.get("show_in_menus", False),
                    )
                    blog_index.add_child(instance=page)
                else:
                    page.title = item["title"]
                    page.excerpt = item.get("excerpt", "")
                    page.topic = item.get("topic", "")
                    page.body = body_value
                    page.published_on = published_on
                    page.owner = author
                    page.show_in_menus = item.get("show_in_menus", False)
                    page.save()

                revision = page.save_revision()

                if item.get("live", True):
                    revision.publish()
                    page.refresh_from_db()

                    if published_at is not None:
                        self._backfill_publish_timestamps(
                            page=page,
                            published_at=published_at,
                        )
                else:
                    if page.live:
                        page.unpublish()

    def _load_seed_data(self):
        seed_data_dir = Path(__file__).resolve().parent.parent / "seed_data" / "dev"

        return {
            "users": self._read_json(seed_data_dir / "users.json"),
            "wagtail_posts": self._read_json(seed_data_dir / "wagtail_posts.json"),
        }

    def _read_json(self, file_path: Path):
        if not file_path.exists():
            raise CommandError(f"Seed data file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _get_blog_index(self):
        site = Site.objects.filter(is_default_site=True).first() or Site.objects.first()
        if site is None:
            raise CommandError("No Wagtail Site record exists after migration.")

        blog_index = BlogIndexPage.objects.child_of(site.root_page).filter(slug="articles").first()
        if blog_index is None:
            raise CommandError(
                "Blog index page '/articles/' was not found after bootstrap_wagtail_blog."
            )

        return blog_index

    def _build_streamfield_value(self, raw_value, post_slug):
        if not isinstance(raw_value, list):
            raise CommandError(
                f"Wagtail post '{post_slug}' has invalid body. Expected a JSON array of blocks."
            )

        body_field = BlogPostPage._meta.get_field("body")

        try:
            return body_field.stream_block.to_python(raw_value)
        except Exception as exc:
            raise CommandError(
                f"Invalid StreamField body for Wagtail post '{post_slug}': {exc}"
            ) from exc

    def _parse_published_at(self, value):
        if value in (None, ""):
            return None

        if value == "now":
            return timezone.now()

        parsed = parse_datetime(value)
        if parsed is None:
            raise CommandError(f"Invalid published_at value in DEV Wagtail seed data: {value}")

        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(parsed, timezone.get_current_timezone())

        return parsed

    def _parse_published_on(self, value, fallback_datetime=None):
        if value not in (None, ""):
            parsed_date = parse_date(value)

            if parsed_date is not None:
                return parsed_date

            parsed_datetime = parse_datetime(value)
            if parsed_datetime is not None:
                return parsed_datetime.date()

            raise CommandError(f"Invalid published_on value in DEV Wagtail seed data: {value}")

        if fallback_datetime is not None:
            return fallback_datetime.date()

        return timezone.localdate()

    def _backfill_publish_timestamps(self, page, published_at):
        fields_to_update = []

        if page.first_published_at != published_at:
            page.first_published_at = published_at
            fields_to_update.append("first_published_at")

        if page.last_published_at != published_at:
            page.last_published_at = published_at
            fields_to_update.append("last_published_at")

        if page.latest_revision_created_at != published_at:
            page.latest_revision_created_at = published_at
            fields_to_update.append("latest_revision_created_at")

        if fields_to_update:
            page.save(update_fields=fields_to_update)

    def _get_required_reference(self, mapping, key, entity_name, post_slug):
        try:
            return mapping[key]
        except KeyError as exc:
            raise CommandError(
                f"Wagtail post '{post_slug}' references missing {entity_name} '{key}' "
                f"in DEV seed data."
            ) from exc
