from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_user_string_representation_returns_username(self):
        user = get_user_model().objects.create_user(username='michal', password='secret123')

        self.assertEqual(str(user), 'michal')

    def test_optional_profile_fields_can_be_blank(self):
        user = get_user_model().objects.create_user(username='blank-user', password='secret123')

        self.assertEqual(user.bio, '')
        self.assertEqual(user.avatar, '')
        self.assertEqual(user.website, '')
