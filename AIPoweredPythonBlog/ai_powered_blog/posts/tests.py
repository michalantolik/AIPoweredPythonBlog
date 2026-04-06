from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from posts.models import Post
from tags.models import Tag


class PostModelTests(TestCase):
    def test_post_string_representation_returns_title(self):
        user = get_user_model().objects.create_user(username='author', password='secret123')
        post = Post.objects.create(
            title='My first post',
            slug='my-first-post',
            author=user,
            content='Hello world',
        )

        self.assertEqual(str(post), 'My first post')

    def test_post_status_defaults_to_draft(self):
        user = get_user_model().objects.create_user(username='author', password='secret123')
        post = Post.objects.create(
            title='Draft post',
            slug='draft-post',
            author=user,
            content='Draft content',
        )

        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertIsNone(post.published_at)


class PostListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='author',
            password='secret123'
        )
        cls.python_tag = Tag.objects.create(name='Python', slug='python')
        cls.django_tag = Tag.objects.create(name='Django', slug='django')
        cls.hidden_tag = Tag.objects.create(name='Hidden', slug='hidden')

        cls.old_post = Post.objects.create(
            title='Old published',
            slug='old-published',
            author=cls.user,
            content='Old content about async Python patterns.',
            excerpt='Async Python notes.',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(days=3),
        )
        cls.old_post.tags.add(cls.python_tag)

        cls.new_post = Post.objects.create(
            title='New published',
            slug='new-published',
            author=cls.user,
            content='New content about Django forms and testing.',
            excerpt='Django testing tips.',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        cls.new_post.tags.add(cls.python_tag, cls.django_tag)

        cls.draft_post = Post.objects.create(
            title='Draft post',
            slug='draft-post',
            author=cls.user,
            content='Draft content',
            status=Post.Status.DRAFT,
        )
        cls.draft_post.tags.add(cls.hidden_tag)

    def test_post_list_returns_only_published_posts_ordered_by_published_at_desc(self):
        response = self.client.get(reverse('posts:list'))

        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.new_post, self.old_post])
        self.assertNotIn(self.draft_post, posts)

    def test_post_list_filters_by_category_slug(self):
        response = self.client.get(reverse('posts:list'), {'category': 'django'})

        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.new_post])
        self.assertEqual(response.context['selected_category'], self.django_tag)

    def test_post_list_filters_by_search_query(self):
        response = self.client.get(reverse('posts:list'), {'q': 'django'})

        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.new_post])
        self.assertEqual(response.context['search_query'], 'django')
        self.assertNotIn(self.old_post, posts)
        self.assertNotIn(self.draft_post, posts)

    def test_post_list_combines_category_and_search_query(self):
        response = self.client.get(reverse('posts:list'), {
            'category': 'python',
            'q': 'async',
        })

        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.old_post])
        self.assertEqual(response.context['selected_category'], self.python_tag)
        self.assertEqual(response.context['search_query'], 'async')

    def test_post_list_search_matches_author_username(self):
        response = self.client.get(reverse('posts:list'), {'q': 'author'})

        self.assertEqual(response.status_code, 200)
        posts = list(response.context['posts'])

        self.assertEqual(posts, [self.new_post, self.old_post])

    def test_post_list_returns_404_for_unknown_category_slug(self):
        response = self.client.get(reverse('posts:list'), {'category': 'missing-category'})

        self.assertEqual(response.status_code, 404)

    def test_post_list_categories_only_include_tags_with_published_posts(self):
        response = self.client.get(reverse('posts:list'))

        categories = list(response.context['categories'])

        self.assertEqual(categories, [self.django_tag, self.python_tag])
        self.assertNotIn(self.hidden_tag, categories)


class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='author',
            password='secret123'
        )
        cls.python_tag = Tag.objects.create(name='Python', slug='python')
        cls.django_tag = Tag.objects.create(name='Django', slug='django')
        cls.extra_tag = Tag.objects.create(name='Extra', slug='extra')

        cls.main_post = Post.objects.create(
            title='Main post',
            slug='main-post',
            author=cls.user,
            content='Main content',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        cls.main_post.tags.add(cls.python_tag, cls.django_tag)

        cls.related_1 = Post.objects.create(
            title='Related 1',
            slug='related-1',
            author=cls.user,
            content='Related content 1',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=1),
        )
        cls.related_1.tags.add(cls.python_tag)

        cls.related_2 = Post.objects.create(
            title='Related 2',
            slug='related-2',
            author=cls.user,
            content='Related content 2',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=2),
        )
        cls.related_2.tags.add(cls.django_tag)

        cls.related_3 = Post.objects.create(
            title='Related 3',
            slug='related-3',
            author=cls.user,
            content='Related content 3',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=3),
        )
        cls.related_3.tags.add(cls.python_tag)

        cls.related_4 = Post.objects.create(
            title='Related 4',
            slug='related-4',
            author=cls.user,
            content='Related content 4',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=4),
        )
        cls.related_4.tags.add(cls.python_tag)

        cls.unrelated_post = Post.objects.create(
            title='Unrelated post',
            slug='unrelated-post',
            author=cls.user,
            content='Unrelated content',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(hours=5),
        )
        cls.unrelated_post.tags.add(cls.extra_tag)

        cls.draft_post = Post.objects.create(
            title='Draft post',
            slug='draft-post',
            author=cls.user,
            content='Draft content',
            status=Post.Status.DRAFT,
        )
        cls.draft_post.tags.add(cls.python_tag)

    def test_post_detail_returns_only_published_post(self):
        response = self.client.get(reverse('posts:detail', args=[self.main_post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.main_post)

    def test_post_detail_returns_404_for_draft_post(self):
        response = self.client.get(reverse('posts:detail', args=[self.draft_post.slug]))

        self.assertEqual(response.status_code, 404)

    def test_post_detail_related_posts_are_tag_based_unique_and_limited_to_three(self):
        response = self.client.get(reverse('posts:detail', args=[self.main_post.slug]))

        related_posts = list(response.context['related_posts'])

        self.assertEqual(related_posts, [self.related_1, self.related_2, self.related_3])
        self.assertNotIn(self.main_post, related_posts)
        self.assertNotIn(self.related_4, related_posts)
        self.assertNotIn(self.unrelated_post, related_posts)
        self.assertEqual(len(related_posts), 3)
