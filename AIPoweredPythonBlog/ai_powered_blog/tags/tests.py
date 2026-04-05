from django.test import TestCase

from tags.models import Tag


class TagModelTests(TestCase):
    def test_tag_string_representation_returns_name(self):
        tag = Tag.objects.create(name='Python', slug='python')

        self.assertEqual(str(tag), 'Python')
