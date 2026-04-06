from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from posts.models import Post
from tags.models import Tag


@override_settings(
    INTRO_OVERLAY_ENABLED=False,
    SHOW_SIDEBAR_ON_HOME_STARTUP=True,
)
class PublicBlogIntegrationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='integration-author',
            password='secret123',
        )

        cls.python_tag = Tag.objects.create(name='Python', slug='python')
        cls.django_tag = Tag.objects.create(name='Django', slug='django')
        cls.architecture_tag = Tag.objects.create(name='Architecture', slug='architecture')
        cls.hidden_tag = Tag.objects.create(name='Hidden', slug='hidden')

        cls.python_patterns_post = Post.objects.create(
            title='Python patterns for APIs',
            slug='python-patterns-for-apis',
            author=cls.user,
            content='Python API content with practical notes.',
            excerpt='A practical Python API article.',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(days=1),
        )
        cls.python_patterns_post.tags.add(cls.python_tag, cls.architecture_tag)

        cls.django_testing_post = Post.objects.create(
            title='Django testing guide',
            slug='django-testing-guide',
            author=cls.user,
            content='Django testing content with integration examples.',
            excerpt='A practical Django testing article.',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        cls.django_testing_post.tags.add(cls.python_tag, cls.django_tag)

        cls.architecture_post = Post.objects.create(
            title='Architecture notes',
            slug='architecture-notes',
            author=cls.user,
            content='Architecture content for related posts testing.',
            excerpt='Architecture article.',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() - timezone.timedelta(days=2),
        )
        cls.architecture_post.tags.add(cls.architecture_tag)

        cls.draft_post = Post.objects.create(
            title='Hidden draft',
            slug='hidden-draft',
            author=cls.user,
            content='Draft content that must stay private.',
            excerpt='Draft excerpt.',
            status=Post.Status.DRAFT,
        )
        cls.draft_post.tags.add(cls.hidden_tag)

    def test_reader_can_browse_home_archive_and_detail_pages(self):
        home_response = self.client.get(reverse('website:home'))

        self.assertEqual(home_response.status_code, 200)
        self.assertTemplateUsed(home_response, 'website/home.html')
        self.assertContains(home_response, 'Django testing guide')
        self.assertContains(home_response, 'Python patterns for APIs')
        self.assertNotContains(home_response, 'Hidden draft')
        self.assertContains(home_response, reverse('posts:list') + '?category=python')

        archive_response = self.client.get(reverse('posts:list'), {'category': 'python'})

        self.assertEqual(archive_response.status_code, 200)
        self.assertTemplateUsed(archive_response, 'posts/list.html')
        self.assertContains(archive_response, 'Django testing guide')
        self.assertContains(archive_response, 'Python patterns for APIs')
        self.assertNotContains(archive_response, 'Architecture notes')
        self.assertNotContains(archive_response, 'Hidden draft')
        self.assertContains(
            archive_response,
            reverse('posts:detail', args=[self.django_testing_post.slug]),
        )

        detail_response = self.client.get(
            reverse('posts:detail', args=[self.django_testing_post.slug])
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertTemplateUsed(detail_response, 'posts/detail.html')
        self.assertContains(detail_response, 'Django testing guide')
        self.assertContains(detail_response, 'A practical Django testing article.')
        self.assertContains(detail_response, 'By integration-author')
        self.assertContains(detail_response, 'Python patterns for APIs')
        self.assertNotContains(detail_response, 'Hidden draft')

    def test_navigation_and_sidebar_expose_only_categories_with_public_content(self):
        response = self.client.get(reverse('posts:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('website:home'))
        self.assertContains(response, reverse('website:about'))
        self.assertContains(response, reverse('posts:list') + '?category=python')
        self.assertContains(response, reverse('posts:list') + '?category=django')
        self.assertContains(response, reverse('posts:list') + '?category=architecture')
        self.assertNotContains(response, reverse('posts:list') + '?category=hidden')
        self.assertNotContains(response, 'Hidden')
        self.assertContains(response, 'All posts')
        self.assertContains(response, 'Full archive')

    @override_settings(LIVE_POST_FILTER_ENABLED=True)
    def test_archive_search_filters_server_side_and_preserves_query_in_links(self):
        response = self.client.get(reverse('posts:list'), {'q': 'django'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/list.html')
        self.assertContains(response, 'Django testing guide')
        self.assertNotContains(response, 'Python patterns for APIs')
        self.assertNotContains(response, 'Architecture notes')
        self.assertContains(response, 'value="django"', html=False)
        self.assertContains(response, 'category=python')
        self.assertContains(response, 'q=django')

    @override_settings(LIVE_POST_FILTER_ENABLED=True)
    def test_archive_search_combines_with_category_filter(self):
        response = self.client.get(reverse('posts:list'), {
            'category': 'python',
            'q': 'api',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python patterns for APIs')
        self.assertNotContains(response, 'Django testing guide')
        self.assertNotContains(response, 'Architecture notes')
        self.assertContains(response, 'value="api"', html=False)

    def test_related_posts_section_shows_only_published_related_articles(self):
        response = self.client.get(reverse('posts:detail', args=[self.python_patterns_post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Related posts')
        self.assertContains(response, 'Django testing guide')
        self.assertContains(response, 'Architecture notes')
        self.assertNotContains(response, 'Hidden draft')
        self.assertEqual(list(response.context['related_posts']), [
            self.django_testing_post,
            self.architecture_post,
        ])

    def test_public_routes_return_404_for_non_public_content_or_invalid_filters(self):
        draft_response = self.client.get(reverse('posts:detail', args=[self.draft_post.slug]))
        missing_category_response = self.client.get(
            reverse('posts:list'),
            {'category': 'missing-category'},
        )

        self.assertEqual(draft_response.status_code, 404)
        self.assertEqual(missing_category_response.status_code, 404)
