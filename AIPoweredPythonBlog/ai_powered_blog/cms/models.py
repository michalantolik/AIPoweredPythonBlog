from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from posts.models import Category
from tags.models import Tag

from .blocks import (
    CalloutBlock,
    CodeBlock,
    FigureBlock,
    MermaidBlock,
    RichSectionBlock,
    SectionHeadingBlock,
)


class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    parent_page_types = ["wagtailcore.Page"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["cms.BlogPostPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = (
            self.get_children()
            .live()
            .public()
            .specific()
            .order_by("-first_published_at")
        )
        return context

    class Meta:
        verbose_name = "Blog index page"


class BlogPostPage(Page):
    excerpt = models.TextField(blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )

    tags = ParentalManyToManyField(
        Tag,
        related_name="blog_posts",
        blank=False,
    )

    body = StreamField(
        [
            ("section_heading", SectionHeadingBlock()),
            (
                "rich_text",
                RichSectionBlock(
                    features=[
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "h2",
                        "h3",
                        "blockquote",
                        "code",
                    ]
                ),
            ),
            ("callout", CalloutBlock()),
            ("code", CodeBlock()),
            ("mermaid", MermaidBlock()),
            ("figure", FigureBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
        index.SearchField("body"),
        index.RelatedFields(
            "author",
            [
                index.SearchField("username"),
                index.SearchField("first_name"),
                index.SearchField("last_name"),
            ],
        ),
        index.RelatedFields(
            "category",
            [
                index.SearchField("name"),
                index.SearchField("slug"),
            ],
        ),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name"),
                index.SearchField("slug"),
            ],
        ),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("excerpt"),
                FieldPanel("author"),
                FieldPanel("category"),
                FieldPanel("tags"),
            ],
            heading="Post settings",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["cms.BlogIndexPage"]

    class Meta:
        verbose_name = "Blog post page"
