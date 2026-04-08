from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from core.seeding.base import seed as base_seed
from posts.models import Category, Post
from tags.models import Tag



def seed():
    """
    DEV seeding.
    Safe place for fake/local/test/demo data.
    """
    with transaction.atomic():
        base_seed()
        seed_dev_blog_data()


def seed_dev_blog_data():
    python_tag, _ = Tag.objects.update_or_create(
        slug="python",
        defaults={"name": "python"},
    )

    django_tag, _ = Tag.objects.update_or_create(
        slug="django",
        defaults={"name": "django"},
    )

    backend_category, _ = Category.objects.update_or_create(
        name="Backend",
        defaults={
            "sort_order": 1,
        },
    )

    user = get_user_model()
    author, _ = user.objects.update_or_create(
        username="devadmin",
        defaults={
            "email": "devadmin@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )

    author.set_password("devpassword123")
    author.save()

    post1, created = Post.objects.update_or_create(
        slug="dev-seed-post-1",
        defaults={
            "title": "DEV Seed Post (1)",
            "excerpt": "This post exists only in DEV seed (1).",
            "content": "DEV seeded content (1).",
            "category": backend_category,
            "author": author,
            "published_at": timezone.now(),
            "status": "published"
        },
    )
    if created:
        post1.tags.add(python_tag, django_tag)

    post2, created = Post.objects.update_or_create(
        slug="dev-seed-post-2",
        defaults={
            "title": "DEV Seed Post (2)",
            "excerpt": "This post exists only in DEV seed (2).",
            "content": "DEV seeded content (2).",
            "category": backend_category,
            "author": author,
            "published_at": timezone.now(),
            "status": "published"
        },
    )
    if created:
        post2.tags.add(python_tag, django_tag)

    post3, created = Post.objects.update_or_create(
        slug="dev-seed-post-3",
        defaults={
            "title": "DEV Seed Post (3)",
            "excerpt": "This post exists only in DEV seed (3).",
            "content": "DEV seeded content (3).",
            "category": backend_category,
            "author": author,
            "published_at": timezone.now(),
            "status": "published"
        },
    )
    if created:
        post3.tags.add(python_tag, django_tag)
