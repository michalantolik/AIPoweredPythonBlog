from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from posts.models import Category, Post
from tags.models import Tag

from .serializers import (
    serialize_category,
    serialize_post_detail,
    serialize_post_summary,
    serialize_tag,
)

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50


def _parse_positive_int(value, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    if parsed < 1:
        return default

    return parsed


def _get_page_size(request) -> int:
    requested_size = _parse_positive_int(request.GET.get("page_size"), DEFAULT_PAGE_SIZE)
    return min(requested_size, MAX_PAGE_SIZE)


@require_GET
def post_list_api(request):
    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-published_at", "-created_at")
    )

    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")

    selected_category = None
    selected_tag = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)

    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    paginator = Paginator(posts.distinct(), _get_page_size(request))
    page_number = _parse_positive_int(request.GET.get("page"), 1)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage as exc:
        raise Http404("Page not found.") from exc

    response_payload = {
        "count": paginator.count,
        "page": page_obj.number,
        "page_size": page_obj.paginator.per_page,
        "num_pages": paginator.num_pages,
        "first_page": 1 if paginator.num_pages > 0 else None,
        "last_page": paginator.num_pages if paginator.num_pages > 0 else None,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "selected_category": serialize_category(selected_category) if selected_category else None,
        "selected_tag": serialize_tag(selected_tag) if selected_tag else None,
        "results": [serialize_post_summary(post) for post in page_obj.object_list],
    }

    return JsonResponse(response_payload)


@require_GET
def post_detail_api(request, slug: str):
    post = get_object_or_404(
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags"),
        slug=slug,
    )

    related_posts = (
        Post.objects.filter(
            status=Post.Status.PUBLISHED,
            category=post.category,
            tags__in=post.tags.all(),
        )
        .exclude(pk=post.pk)
        .select_related("author", "category")
        .prefetch_related("tags")
        .distinct()
        .order_by("-published_at", "-created_at")[:3]
    )

    response_payload = serialize_post_detail(post)
    response_payload["related_posts"] = [serialize_post_summary(item) for item in related_posts]

    return JsonResponse(response_payload)


@require_GET
def tag_list_api(request):
    tags = (
        Tag.objects.filter(posts__status=Post.Status.PUBLISHED)
        .distinct()
        .order_by("name")
    )

    response_payload = {
        "count": tags.count(),
        "results": [serialize_tag(tag) for tag in tags],
    }

    return JsonResponse(response_payload)
