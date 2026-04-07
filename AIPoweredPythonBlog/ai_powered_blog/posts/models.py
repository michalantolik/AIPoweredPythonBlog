from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from tags.models import Tag


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    sort_order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        null=True,
        blank=True,
    )

    content = models.TextField()
    excerpt = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    tags = models.ManyToManyField(Tag, related_name="posts")

    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
