from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

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
    topic = models.CharField(max_length=80, blank=True)
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("section_heading", SectionHeadingBlock()),
            ("rich_text", RichSectionBlock(features=[
                "bold",
                "italic",
                "link",
                "ol",
                "ul",
                "h2",
                "h3",
                "blockquote",
                "code",
            ])),
            ("callout", CalloutBlock()),
            ("code", CodeBlock()),
            ("mermaid", MermaidBlock()),
            ("figure", FigureBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    published_on = models.DateField(default=timezone.now)

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
        index.SearchField("topic"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("excerpt"),
                FieldPanel("topic"),
                FieldPanel("cover_image"),
                FieldPanel("published_on"),
            ],
            heading="Post settings",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["cms.BlogIndexPage"]

    class Meta:
        verbose_name = "Blog post page"
