import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from users.models import User
from tags.models import Tag
from posts.models import Post
from comments.models import Comment


class Command(BaseCommand):
    help = "Seed database with demo users, tags, posts, and comments"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting seed..."))

        users = self._seed_users()
        tags = self._seed_tags()
        posts = self._seed_posts(users, tags)
        self._seed_comments(users, posts)

        self.stdout.write(self.style.SUCCESS("Seeding finished successfully."))

    def _seed_users(self):
        self.stdout.write("Seeding users...")

        users_data = [
            {
                "username": "michal_dev",
                "email": "michal@example.com",
                "bio": "Software developer writing about Django and architecture.",
                "website": "https://example.com/michal",
                "avatar": "https://picsum.photos/seed/michal/200/200",
            },
            {
                "username": "anna_arch",
                "email": "anna@example.com",
                "bio": "Clean architecture enthusiast.",
                "website": "https://example.com/anna",
                "avatar": "https://picsum.photos/seed/anna/200/200",
            },
            {
                "username": "tom_python",
                "email": "tom@example.com",
                "bio": "Python backend developer.",
                "website": "https://example.com/tom",
                "avatar": "https://picsum.photos/seed/tom/200/200",
            },
            {
                "username": "kate_testing",
                "email": "kate@example.com",
                "bio": "I like tests, quality, and automation.",
                "website": "https://example.com/kate",
                "avatar": "https://picsum.photos/seed/kate/200/200",
            },
            {
                "username": "john_cloud",
                "email": "john@example.com",
                "bio": "Cloud and infrastructure notes.",
                "website": "https://example.com/john",
                "avatar": "https://picsum.photos/seed/john/200/200",
            },
            {
                "username": "eva_data",
                "email": "eva@example.com",
                "bio": "Data, APIs, and practical engineering.",
                "website": "https://example.com/eva",
                "avatar": "https://picsum.photos/seed/eva/200/200",
            },
        ]

        users = []

        for item in users_data:
            user, created = User.objects.get_or_create(
                username=item["username"],
                defaults={
                    "email": item["email"],
                    "bio": item["bio"],
                    "website": item["website"],
                    "avatar": item["avatar"],
                },
            )

            if created:
                user.set_password("Demo12345!")
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                updated = False

                if user.email != item["email"]:
                    user.email = item["email"]
                    updated = True
                if user.bio != item["bio"]:
                    user.bio = item["bio"]
                    updated = True
                if user.website != item["website"]:
                    user.website = item["website"]
                    updated = True
                if user.avatar != item["avatar"]:
                    user.avatar = item["avatar"]
                    updated = True

                if updated:
                    user.save()
                    self.stdout.write(f"Updated user: {user.username}")
                else:
                    self.stdout.write(f"User already exists: {user.username}")

            users.append(user)

        return users

    def _seed_tags(self):
        self.stdout.write("Seeding tags...")

        tag_names = [
            "python",
            "django",
            "architecture",
            "backend",
            "testing",
            "api",
            "clean-code",
            "database",
        ]

        tags = []

        for name in tag_names:
            slug = slugify(name)
            tag, created = Tag.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created tag: {tag.name}"))
            else:
                self.stdout.write(f"Tag already exists: {tag.name}")

            tags.append(tag)

        return tags

    def _seed_posts(self, users, tags):
        self.stdout.write("Seeding posts...")

        posts_data = [
            {
                "title": "Getting Started with Django",
                "excerpt": "A simple introduction to Django project structure.",
                "content": "This is a demo post about Django basics, project structure, apps, templates, and urls.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Clean Architecture for Small Projects",
                "excerpt": "How to keep code simple and organized.",
                "content": "This post explains practical clean architecture ideas for small and medium web apps.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Why Good Naming Matters",
                "excerpt": "Good naming makes code easier to read.",
                "content": "This article covers naming in models, views, templates, and services.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Testing Django Views",
                "excerpt": "Start with the most important flows.",
                "content": "This post shows a minimal approach to testing list pages, detail pages, and forms.",
                "status": Post.Status.DRAFT,
            },
            {
                "title": "Simple Blog Layout Ideas",
                "excerpt": "A clean layout for a technical blog.",
                "content": "This article describes a practical layout with base template, nav, content area, and footer.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Working with Slugs in Django",
                "excerpt": "How and why to use slugs.",
                "content": "This post explains slug generation, uniqueness, and routing.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Database Design Basics",
                "excerpt": "Small practical rules for tables and relations.",
                "content": "This article discusses foreign keys, many-to-many tables, and consistent schema naming.",
                "status": Post.Status.PUBLISHED,
            },
            {
                "title": "Building a Posts List Page",
                "excerpt": "How to show posts in a clean way.",
                "content": "This post covers list views, template loops, and simple styling.",
                "status": Post.Status.DRAFT,
            },
        ]

        posts = []

        for index, item in enumerate(posts_data):
            slug = slugify(item["title"])
            author = users[index % len(users)]

            post, created = Post.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": item["title"],
                    "author": author,
                    "content": item["content"],
                    "excerpt": item["excerpt"],
                    "status": item["status"],
                    "published_at": timezone.now() if item["status"] == Post.Status.PUBLISHED else None,
                },
            )

            if created:
                selected_tags = random.sample(tags, k=random.randint(2, 4))
                post.tags.set(selected_tags)
                self.stdout.write(self.style.SUCCESS(f"Created post: {post.title}"))
            else:
                changed = False

                if post.title != item["title"]:
                    post.title = item["title"]
                    changed = True
                if post.author != author:
                    post.author = author
                    changed = True
                if post.content != item["content"]:
                    post.content = item["content"]
                    changed = True
                if post.excerpt != item["excerpt"]:
                    post.excerpt = item["excerpt"]
                    changed = True
                if post.status != item["status"]:
                    post.status = item["status"]
                    changed = True

                desired_published_at = timezone.now() if item["status"] == Post.Status.PUBLISHED else None
                if (post.published_at is None) != (desired_published_at is None):
                    post.published_at = desired_published_at
                    changed = True

                if changed:
                    post.save()

                if post.tags.count() == 0:
                    selected_tags = random.sample(tags, k=random.randint(2, 4))
                    post.tags.set(selected_tags)

                self.stdout.write(f"Post already exists: {post.title}")

            posts.append(post)

        return posts

    def _seed_comments(self, users, posts):
        self.stdout.write("Seeding comments...")

        comment_texts = [
            "Very useful post. Clear and practical.",
            "I like this explanation. Simple and clean.",
            "Good summary. Easy to follow.",
            "Nice article. This helped me understand the topic better.",
            "I would like to read part two of this.",
            "This is exactly the kind of practical content I need.",
            "Great structure and clean examples.",
            "Short, direct, and helpful.",
            "This topic is explained very well here.",
            "Thanks, this gave me a good starting point.",
        ]

        created_count = 0

        for i in range(10):
            post = posts[i % len(posts)]
            author = users[(i + 1) % len(users)]
            content = comment_texts[i]

            comment_exists = Comment.objects.filter(
                post=post,
                author=author,
                content=content,
            ).exists()

            if comment_exists:
                self.stdout.write(f"Comment already exists for post: {post.title}")
                continue

            Comment.objects.create(
                post=post,
                author=author,
                content=content,
                is_approved=(i % 4 != 0),
            )

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created comment #{created_count}"))

        self.stdout.write(self.style.SUCCESS("Comments ready"))
