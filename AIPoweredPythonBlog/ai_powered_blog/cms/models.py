from django.conf import settings
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, Q
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
    PlantUMLBlock,
    RichSectionBlock,
    SectionHeadingBlock,
)


class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["cms.BlogPostPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    POSTS_PER_PAGE = 6

    def get_posts_queryset(self):
        return (
            BlogPostPage.objects.child_of(self)
            .live()
            .public()
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-first_published_at")
        )

    def get_sidebar_categories(self):
        return (
            Category.objects.annotate(
                published_posts_count=Count(
                    "blog_posts",
                    filter=Q(blog_posts__live=True),
                    distinct=True,
                )
            )
            .filter(published_posts_count__gt=0)
            .order_by("sort_order", "name")
        )

    def get_context(self, request):
        context = super().get_context(request)

        category_slug = request.GET.get("category", "").strip()
        categories = self.get_sidebar_categories()
        posts = self.get_posts_queryset()
        selected_category = None

        if category_slug:
            selected_category = categories.filter(slug=category_slug).first()
            if selected_category:
                posts = posts.filter(category=selected_category)

        paginator = Paginator(posts, self.POSTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        query_params.pop("page", None)

        context["posts"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["pagination_query_string"] = query_params.urlencode()
        context["categories"] = categories
        context["selected_category"] = selected_category
        context["sidebar_base_url"] = self.url
        context["blog_index_url"] = self.url
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
            ("plantuml", PlantUMLBlock()),
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
