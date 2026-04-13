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

    @staticmethod
    def build_query_string(request, **updates):
        query_params = request.GET.copy()
        query_params.pop("page", None)

        for key, value in updates.items():
            if value in (None, ""):
                query_params.pop(key, None)
            else:
                query_params[key] = value

        return query_params.urlencode()

    @staticmethod
    def get_page_numbers(page_obj, radius=2):
        current = page_obj.number
        total = page_obj.paginator.num_pages

        start = max(current - radius, 1)
        end = min(current + radius, total)

        return range(start, end + 1)

    def get_context(self, request):
        context = super().get_context(request)

        category_slug = request.GET.get("category", "").strip()
        tag_slug = request.GET.get("tag", "").strip()
        search_query = request.GET.get("q", "").strip()

        categories = self.get_sidebar_categories()
        posts = self.get_posts_queryset()

        selected_category = None
        selected_tag = None

        if category_slug:
            selected_category = categories.filter(slug=category_slug).first()
            if selected_category:
                posts = posts.filter(category=selected_category)

        if tag_slug:
            selected_tag = Tag.objects.filter(slug=tag_slug).first()
            if selected_tag:
                posts = posts.filter(tags=selected_tag)

        if search_query:
            search_terms = search_query.split()

            for term in search_terms:
                posts = posts.filter(
                    Q(title__icontains=term)
                    | Q(excerpt__icontains=term)
                    | Q(search_description__icontains=term)
                    | Q(author__username__icontains=term)
                    | Q(category__name__icontains=term)
                    | Q(tags__name__icontains=term)
                )

            posts = posts.distinct()

        paginator = Paginator(posts, self.POSTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["posts"] = page_obj.object_list
        context["page_obj"] = page_obj
        context["page_numbers"] = self.get_page_numbers(page_obj)
        context["pagination_query_string"] = self.build_query_string(request)
        context["pagination_base_url"] = self.url
        context["categories"] = categories
        context["selected_category"] = selected_category
        context["selected_tag"] = selected_tag
        context["search_query"] = search_query
        context["sidebar_base_url"] = self.url
        context["blog_index_url"] = self.url
        context["all_posts_query_string"] = self.build_query_string(
            request,
            category="",
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
