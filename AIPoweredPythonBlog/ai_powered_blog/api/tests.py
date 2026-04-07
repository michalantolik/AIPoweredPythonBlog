from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Category, Post
from tags.models import Tag


class PostApiTests(TestCase):
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

        cls.python_tag = Tag.objects.create(name="Python", slug="python")
        cls.django_tag = Tag.objects.create(name="Django", slug="django")
        cls.hidden_tag = Tag.objects.create(name="Hidden", slug="hidden")

        cls.first_post = Post.objects.create(
            title="First published",
            slug="first-published",
            author=cls.user,
            category=cls.python_category,
            content="First content",
            excerpt="First excerpt",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(days=1),
        )
        cls.first_post.tags.add(cls.python_tag)

        cls.second_post = Post.objects.create(
            title="Second published",
            slug="second-published",
            author=cls.user,
            category=cls.architecture_category,
            content="Second content",
            excerpt="Second excerpt",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        cls.second_post.tags.add(cls.python_tag, cls.django_tag)

        cls.draft_post = Post.objects.create(
            title="Draft post",
            slug="draft-post",
            author=cls.user,
            category=cls.architecture_category,
            content="Draft content",
            excerpt="Draft excerpt",
            status=Post.Status.DRAFT,
        )
        cls.draft_post.tags.add(cls.hidden_tag)

    def test_post_list_api_returns_published_posts_only(self):
        response = self.client.get(reverse("api:post-list"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["count"], 2)
        self.assertEqual(
            [item["slug"] for item in payload["results"]],
            ["second-published", "first-published"],
        )
        self.assertEqual(payload["results"][0]["category"]["slug"], "architecture-and-patterns")

    def test_post_list_api_filters_by_category(self):
        response = self.client.get(reverse("api:post-list"), {"category": "python-ecosystem"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["selected_category"]["slug"], "python-ecosystem")
        self.assertEqual(payload["results"][0]["slug"], "first-published")

    def test_post_list_api_filters_by_tag(self):
        response = self.client.get(reverse("api:post-list"), {"tag": "django"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["selected_tag"]["slug"], "django")
        self.assertEqual(payload["results"][0]["slug"], "second-published")

    def test_post_list_api_returns_404_for_unknown_category(self):
        response = self.client.get(reverse("api:post-list"), {"category": "missing"})

        self.assertEqual(response.status_code, 404)

    def test_post_list_api_returns_404_for_unknown_tag(self):
        response = self.client.get(reverse("api:post-list"), {"tag": "missing"})

        self.assertEqual(response.status_code, 404)

    def test_post_list_api_paginates_results(self):
        response = self.client.get(reverse("api:post-list"), {"page_size": 1, "page": 2})

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["page"], 2)
        self.assertEqual(payload["page_size"], 1)
        self.assertEqual(payload["num_pages"], 2)
        self.assertEqual(payload["results"][0]["slug"], "first-published")

    def test_post_list_api_returns_404_for_page_out_of_range(self):
        response = self.client.get(reverse("api:post-list"), {"page": 99})

        self.assertEqual(response.status_code, 404)

    def test_post_detail_api_returns_post_and_related_posts(self):
        related_post = Post.objects.create(
            title="Related post",
            slug="related-post",
            author=self.user,
            category=self.architecture_category,
            content="Related content",
            excerpt="Related excerpt",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=1),
        )
        related_post.tags.add(self.python_tag)

        unrelated_post = Post.objects.create(
            title="Unrelated post",
            slug="unrelated-post",
            author=self.user,
            category=self.python_category,
            content="Unrelated content",
            excerpt="Unrelated excerpt",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=2),
        )
        unrelated_post.tags.add(self.python_tag)

        response = self.client.get(reverse("api:post-detail", args=[self.second_post.slug]))

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["slug"], "second-published")
        self.assertEqual(payload["content"], "Second content")
        self.assertEqual(payload["category"]["slug"], "architecture-and-patterns")
        self.assertEqual(
            [item["slug"] for item in payload["related_posts"]],
            ["related-post"],
        )
        self.assertNotIn("unrelated-post", [item["slug"] for item in payload["related_posts"]])

    def test_post_detail_api_returns_404_for_draft_post(self):
        response = self.client.get(reverse("api:post-detail", args=[self.draft_post.slug]))

        self.assertEqual(response.status_code, 404)


class TagApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            username="author",
            password="secret123",
        )

        category = Category.objects.create(
            name="Python Ecosystem",
            slug="python-ecosystem",
            sort_order=2,
        )

        cls.python_tag = Tag.objects.create(name="Python", slug="python")
        cls.hidden_tag = Tag.objects.create(name="Hidden", slug="hidden")

        post = Post.objects.create(
            title="Published post",
            slug="published-post",
            author=user,
            category=category,
            content="Content",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        post.tags.add(cls.python_tag)

        draft_post = Post.objects.create(
            title="Draft post",
            slug="draft-post",
            author=user,
            category=category,
            content="Draft content",
            status=Post.Status.DRAFT,
        )
        draft_post.tags.add(cls.hidden_tag)

    def test_tag_list_api_returns_only_tags_used_by_published_posts(self):
        response = self.client.get(reverse("api:tag-list"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"], [{"name": "Python", "slug": "python"}])
