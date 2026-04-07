from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Category, Post
from tags.models import Tag


class WebsiteViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="author",
            password="secret123",
        )

        cls.python_category = Category.objects.create(
            name="Python Ecosystem",
            slug="python-ecosystem",
            sort_order=2,
        )
        cls.architecture_category = Category.objects.create(
            name="Architecture and Patterns",
            slug="architecture-and-patterns",
            sort_order=7,
        )
        cls.hidden_category = Category.objects.create(
            name="Cloud (Azure & AWS)",
            slug="cloud-azure-aws",
            sort_order=3,
        )

        cls.python_tag = Tag.objects.create(name="Python", slug="python")
        cls.django_tag = Tag.objects.create(name="Django", slug="django")
        cls.hidden_tag = Tag.objects.create(name="Hidden", slug="hidden")

        for index in range(7):
            post = Post.objects.create(
                title=f"Published post {index}",
                slug=f"published-post-{index}",
                author=cls.user,
                category=cls.python_category if index < 6 else cls.architecture_category,
                content=f"Content {index}",
                status=Post.Status.PUBLISHED,
                published_at=timezone.now() - timezone.timedelta(minutes=index),
            )
            post.tags.add(cls.python_tag if index < 6 else cls.django_tag)

        cls.draft_post = Post.objects.create(
            title="Draft post",
            slug="draft-post",
            author=cls.user,
            category=cls.hidden_category,
            content="Draft content",
            status=Post.Status.DRAFT,
        )
        cls.draft_post.tags.add(cls.hidden_tag)

    def test_home_view_returns_latest_six_published_posts_only(self):
        response = self.client.get(reverse("website:home"))

        self.assertEqual(response.status_code, 200)
        latest_posts = list(response.context["latest_posts"])

        self.assertEqual(len(latest_posts), 6)
        self.assertTrue(all(post.status == Post.Status.PUBLISHED for post in latest_posts))
        self.assertNotIn(self.draft_post, latest_posts)

    def test_home_view_categories_only_include_categories_with_published_posts(self):
        response = self.client.get(reverse("website:home"))

        categories = list(response.context["categories"])

        self.assertEqual(categories, [self.python_category, self.architecture_category])
        self.assertNotIn(self.hidden_category, categories)

    def test_about_view_renders_successfully_with_categories(self):
        response = self.client.get(reverse("website:about"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("categories", response.context)
