from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from tags.models import Tag
from .models import Category, Post
from .selectors import get_sidebar_categories

POSTS_PER_PAGE = 6


def _build_pagination_query_string(request) -> str:
    query_params = request.GET.copy()
    query_params.pop("page", None)
    return query_params.urlencode()


def post_list(request):
    category_slug = request.GET.get("category", "").strip()
    tag_slug = request.GET.get("tag", "").strip()
    live_post_filter_enabled = getattr(settings, "LIVE_POST_FILTER_ENABLED", False)
    search_query = request.GET.get("q", "").strip() if live_post_filter_enabled else ""

    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-published_at", "-created_at")
    )

    selected_category = None
    selected_tag = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)

    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    if search_query:
        search_terms = search_query.split()

        for term in search_terms:
            posts = posts.filter(
                Q(title__icontains=term)
                | Q(excerpt__icontains=term)
                | Q(content__icontains=term)
                | Q(author__username__icontains=term)
                | Q(category__name__icontains=term)
                | Q(tags__name__icontains=term)
            )

        posts = posts.distinct()

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "categories": get_sidebar_categories(),
        "selected_category": selected_category,
        "selected_tag": selected_tag,
        "search_query": search_query,
        "pagination_query_string": _build_pagination_query_string(request),
    }
    return render(request, "posts/list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author", "category").prefetch_related("tags"),
        slug=slug,
        status=Post.Status.PUBLISHED,
    )

    related_posts = (
        Post.objects.filter(
            status=Post.Status.PUBLISHED,
            category=post.category,
            tags__in=post.tags.all(),
        )
        .exclude(id=post.id)
        .select_related("author", "category")
        .prefetch_related("tags")
        .distinct()
        .order_by("-published_at", "-created_at")[:3]
    )

    context = {
        "post": post,
        "related_posts": related_posts,
        "categories": get_sidebar_categories(),
    }
    return render(request, "posts/detail.html", context)
