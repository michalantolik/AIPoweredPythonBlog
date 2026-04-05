from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from core.context_processors import site_ui_settings
from core.models import TimeStampedModel
from posts.models import Post
from users.models import User


class TimeStampedModelTests(TestCase):
    def test_timestamp_fields_are_populated_on_create(self):
        user = User.objects.create_user(username='author', password='secret123')
        post = Post.objects.create(
            title='Timestamped post',
            slug='timestamped-post',
            author=user,
            content='Content',
        )

        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)
        self.assertLessEqual(post.created_at, timezone.now())
        self.assertLessEqual(post.updated_at, timezone.now())

    def test_timestamp_model_is_abstract(self):
        self.assertTrue(TimeStampedModel._meta.abstract)


class SiteUiSettingsContextProcessorTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    @override_settings(
        INTRO_OVERLAY_ENABLED=True,
        INTRO_OVERLAY_DURATION_MS=4500,
        INTRO_OVERLAY_IMAGE='images/custom-intro.png',
        SHOW_SIDEBAR_ON_HOME_STARTUP=True,
    )
    def test_context_processor_uses_settings_values(self):
        context = site_ui_settings(self.request)

        self.assertEqual(
            context,
            {
                'INTRO_OVERLAY_ENABLED': True,
                'INTRO_OVERLAY_DURATION_MS': 4500,
                'INTRO_OVERLAY_IMAGE': 'images/custom-intro.png',
                'SHOW_SIDEBAR_ON_HOME_STARTUP': True,
            }
        )

    @override_settings()
    def test_context_processor_falls_back_to_safe_defaults_when_settings_missing(self):
        from django.conf import settings

        for attr in (
            'INTRO_OVERLAY_ENABLED',
            'INTRO_OVERLAY_DURATION_MS',
            'INTRO_OVERLAY_IMAGE',
            'SHOW_SIDEBAR_ON_HOME_STARTUP',
        ):
            if hasattr(settings, attr):
                delattr(settings, attr)

        context = site_ui_settings(self.request)

        self.assertEqual(context['INTRO_OVERLAY_ENABLED'], False)
        self.assertEqual(context['INTRO_OVERLAY_DURATION_MS'], 3200)
        self.assertEqual(context['INTRO_OVERLAY_IMAGE'], 'images/intro/michal-portrait.png')
        self.assertEqual(context['SHOW_SIDEBAR_ON_HOME_STARTUP'], False)
