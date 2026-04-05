from django.contrib.auth import get_user_model
from django.test import TestCase

from comments.models import Comment
from posts.models import Post


class CommentModelTests(TestCase):
    def test_comment_defaults_to_approved_and_has_readable_string(self):
        user = get_user_model().objects.create_user(username='author', password='secret123')
        post = Post.objects.create(
            title='Post title',
            slug='post-title',
            author=user,
            content='Post content',
        )

        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Nice article',
        )

        self.assertTrue(comment.is_approved)
        self.assertEqual(str(comment), f'Comment by {user}')
        self.assertEqual(comment.post, post)
