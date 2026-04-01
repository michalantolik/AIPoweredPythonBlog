from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from posts.models import Post


class Comment(TimeStampedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author}'
