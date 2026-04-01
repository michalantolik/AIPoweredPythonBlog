from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from tags.models import Tag


class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    content = models.TextField()  # markdown later
    excerpt = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
