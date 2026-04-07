from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.seeding.category_seed_data import seed_categories
from posts.models import Category, Post
from tags.models import Tag


class Command(BaseCommand):
    help = "Seed deterministic public data for Playwright smoke tests."

    def handle(self, *args, **options):
        User = get_user_model()

        author, _ = User.objects.get_or_create(
            username="smoke_author",
            defaults={
                "email": "smoke@example.com",
            },
        )

        author.set_password("Demo12345!")
        author.save(update_fields=["password"])

        categories = seed_categories(Category, self.stdout, self.style)

        python_tag, _ = Tag.objects.get_or_create(name="Python", slug="python")
        testing_tag, _ = Tag.objects.get_or_create(name="Testing", slug="testing")
        django_tag, _ = Tag.objects.get_or_create(name="Django", slug="django")
        hidden_tag, _ = Tag.objects.get_or_create(name="Hidden", slug="hidden")

        smoke_post, _ = Post.objects.update_or_create(
            slug="smoke-test-post",
            defaults={
                "title": "Smoke Test Post",
                "author": author,
                "category": categories["python-ecosystem"],
                "content": (
                    "This post is used by Playwright to verify that the public blog pages "
                    "render correctly from the browser perspective."
                ),
                "excerpt": "Stable excerpt for browser smoke tests.",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
            },
        )
        smoke_post.tags.set([python_tag, testing_tag])

        related_post, _ = Post.objects.update_or_create(
            slug="smoke-related-post",
            defaults={
                "title": "Smoke Related Post",
                "author": author,
                "category": categories["python-ecosystem"],
                "content": "A related public article used to validate the related posts section.",
                "excerpt": "Related post visible from the smoke detail page.",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(hours=1),
            },
        )
        related_post.tags.set([python_tag])

        archive_post, _ = Post.objects.update_or_create(
            slug="archive-smoke-post",
            defaults={
                "title": "Archive Smoke Post",
                "author": author,
                "category": categories["python-ecosystem"],
                "content": "Another public article to make the archive page look realistic.",
                "excerpt": "Archive coverage for Playwright smoke tests.",
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(hours=2),
            },
        )
        archive_post.tags.set([django_tag])

        hidden_post, _ = Post.objects.update_or_create(
            slug="hidden-smoke-draft",
            defaults={
                "title": "Hidden Smoke Draft",
                "author": author,
                "category": categories["architecture-and-patterns"],
                "content": "Draft-only post that must never appear on public pages.",
                "excerpt": "This excerpt should stay private.",
                "status": Post.Status.DRAFT,
                "published_at": None,
            },
        )
        hidden_post.tags.set([hidden_tag])

        self.stdout.write(self.style.SUCCESS("Playwright smoke data seeded."))
