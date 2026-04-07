from django.utils import timezone
from django.utils.text import slugify

from comments.models import Comment
from core.seeding.category_seed_data import seed_categories
from posts.models import Category, Post
from tags.models import Tag
from users.models import User


def run_dev_seed(stdout, style):
    stdout.write("Seeding dev users...")
    users = _seed_dev_users(stdout, style)

    stdout.write("Seeding categories...")
    categories = seed_categories(Category, stdout, style)

    stdout.write("Seeding dev posts...")
    posts = _seed_dev_posts(users, categories, stdout, style)

    stdout.write("Seeding dev comments...")
    _seed_dev_comments(users, posts, stdout, style)


def _seed_dev_users(stdout, style):
    users_data = [
        {
            "username": "michal_dev",
            "email": "michal@example.com",
            "bio": "Software developer writing about architecture, cloud, DevOps, and application design.",
            "website": "https://example.com/michal",
            "avatar": "https://picsum.photos/seed/michal/200/200",
            "password": "Demo12345!",
        },
        {
            "username": "anna_arch",
            "email": "anna@example.com",
            "bio": "Architecture and patterns enthusiast.",
            "website": "https://example.com/anna",
            "avatar": "https://picsum.photos/seed/anna/200/200",
            "password": "Demo12345!",
        },
        {
            "username": "tom_python",
            "email": "tom@example.com",
            "bio": "Python backend developer.",
            "website": "https://example.com/tom",
            "avatar": "https://picsum.photos/seed/tom/200/200",
            "password": "Demo12345!",
        },
        {
            "username": "kate_testing",
            "email": "kate@example.com",
            "bio": "I like tests, quality, CI/CD, and automation.",
            "website": "https://example.com/kate",
            "avatar": "https://picsum.photos/seed/kate/200/200",
            "password": "Demo12345!",
        },
        {
            "username": "john_cloud",
            "email": "john@example.com",
            "bio": "Cloud and infrastructure notes.",
            "website": "https://example.com/john",
            "avatar": "https://picsum.photos/seed/john/200/200",
            "password": "Demo12345!",
        },
        {
            "username": "eva_data",
            "email": "eva@example.com",
            "bio": "APIs, backend systems, and practical engineering.",
            "website": "https://example.com/eva",
            "avatar": "https://picsum.photos/seed/eva/200/200",
            "password": "Demo12345!",
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

        if created or updated:
            user.set_password(item["password"])
            user.save()

        if created:
            stdout.write(style.SUCCESS(f"Created dev user: {user.username}"))
        elif updated:
            stdout.write(f"Updated dev user: {user.username}")
        else:
            stdout.write(f"Dev user already exists: {user.username}")

        users.append(user)

    return users


def _get_or_create_tags(tag_names):
    tags = []

    for name in tag_names:
        normalized_name = name.strip()
        tag, _ = Tag.objects.get_or_create(
            slug=slugify(normalized_name),
            defaults={"name": normalized_name},
        )

        if tag.name != normalized_name:
            tag.name = normalized_name
            tag.save(update_fields=["name"])

        tags.append(tag)

    return tags


def _seed_dev_posts(users, categories, stdout, style):
    now = timezone.now()

    posts_data = [
        {
            "title": "Dependency Injection Lifetimes in ASP.NET Core",
            "excerpt": "A practical guide to singleton, scoped, and transient services in .NET.",
            "content": (
                "This post explains dependency injection lifetimes in ASP.NET Core. "
                "It covers singleton, scoped, and transient services, common mistakes, "
                "and how service lifetime choices affect C# web applications."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=10),
            "category_slug": "dotnet-ecosystem",
            "tags": ["ASP.NET Core", "Dependency Injection", "C#", "Service Lifetimes"],
        },
        {
            "title": "Background Jobs in Django with Celery",
            "excerpt": "How to move slow work out of the request cycle in Python applications.",
            "content": (
                "This article shows how Django teams can use Celery and Redis for background jobs. "
                "It covers asynchronous task execution, retry patterns, and keeping Python web apps responsive."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=8),
            "category_slug": "python-ecosystem",
            "tags": ["Django", "Celery", "Redis", "Background Jobs"],
        },
        {
            "title": "Azure App Service vs AWS Elastic Beanstalk for Small Teams",
            "excerpt": "A simple comparison of two cloud hosting options for web projects.",
            "content": (
                "This post compares Azure App Service and AWS Elastic Beanstalk. "
                "It focuses on deployment simplicity, operational effort, pricing considerations, "
                "and where each cloud platform fits best."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=7),
            "category_slug": "cloud-azure-aws",
            "tags": ["Azure", "AWS", "App Service", "Elastic Beanstalk", "Cloud Hosting"],
        },
        {
            "title": "GitHub Actions Pipeline for Django and Pytest",
            "excerpt": "A clean CI/CD workflow for running tests and checks automatically.",
            "content": (
                "This article explains how to build a GitHub Actions pipeline for Django projects. "
                "It covers automation, pytest execution, linting hooks, and practical CI/CD structure."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=5),
            "category_slug": "devops-automation",
            "tags": ["GitHub Actions", "CI/CD", "Pytest", "Automation"],
        },
        {
            "title": "Dockerizing Django for Local Development and CI",
            "excerpt": "A practical Docker setup for consistent development environments.",
            "content": (
                "This post explains how to containerize a Django application with Docker and Docker Compose. "
                "It covers local development, repeatable environments, image structure, and CI-friendly builds."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=4),
            "category_slug": "containers-and-kubernetes",
            "tags": ["Docker", "Docker Compose", "Django", "Containers"],
        },
        {
            "title": "Getting Started with Terraform for Azure Resource Groups",
            "excerpt": "A first Infrastructure as Code workflow for Azure teams.",
            "content": (
                "This article introduces Terraform for Azure resource groups. "
                "It explains Infrastructure as Code basics, reusable configuration, and safer environment provisioning."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=3),
            "category_slug": "infrastructure-as-code",
            "tags": ["Terraform", "Azure", "Infrastructure as Code", "Resource Groups"],
        },
        {
            "title": "Vertical Slice Architecture in Real Projects",
            "excerpt": "Why feature-based structure often works better than technical layers.",
            "content": (
                "This post explores vertical slice architecture, modular thinking, and practical patterns "
                "for real business systems. It compares slice-based organization with classic layered designs."
            ),
            "status": Post.Status.PUBLISHED,
            "published_at": now - timezone.timedelta(days=2),
            "category_slug": "architecture-and-patterns",
            "tags": ["Architecture", "Vertical Slice", "Modular Monolith", "Patterns"],
        },
        {
            "title": "Kubernetes Readiness and Liveness Probes Explained",
            "excerpt": "What probes do and how they help stable container orchestration.",
            "content": (
                "This draft explains Kubernetes readiness probes and liveness probes. "
                "It covers containers, pod health checks, restart behavior, and troubleshooting basics."
            ),
            "status": Post.Status.DRAFT,
            "published_at": None,
            "category_slug": "containers-and-kubernetes",
            "tags": ["Kubernetes", "Readiness Probe", "Liveness Probe", "Containers"],
        },
    ]

    posts = []

    for index, item in enumerate(posts_data):
        slug = slugify(item["title"])
        author = users[index % len(users)]
        category = categories[item["category_slug"]]

        post, created = Post.objects.get_or_create(
            slug=slug,
            defaults={
                "title": item["title"],
                "author": author,
                "category": category,
                "content": item["content"],
                "excerpt": item["excerpt"],
                "status": item["status"],
                "published_at": item["published_at"],
            },
        )

        changed = False

        if post.title != item["title"]:
            post.title = item["title"]
            changed = True
        if post.author != author:
            post.author = author
            changed = True
        if post.category != category:
            post.category = category
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
        if post.published_at != item["published_at"]:
            post.published_at = item["published_at"]
            changed = True

        if created or changed:
            post.save()

        desired_tags = _get_or_create_tags(item["tags"])
        post.tags.set(desired_tags)

        if created:
            stdout.write(style.SUCCESS(f"Created dev post: {post.title}"))
        elif changed:
            stdout.write(f"Updated dev post: {post.title}")
        else:
            stdout.write(f"Dev post already exists: {post.title}")

        posts.append(post)

    return posts


def _seed_dev_comments(users, posts, stdout, style):
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
            stdout.write(f"Dev comment already exists for post: {post.title}")
            continue

        Comment.objects.create(
            post=post,
            author=author,
            content=content,
            is_approved=(i % 4 != 0),
        )

        created_count += 1
        stdout.write(style.SUCCESS(f"Created dev comment #{created_count}"))

    stdout.write(style.SUCCESS("Dev comments ready"))
