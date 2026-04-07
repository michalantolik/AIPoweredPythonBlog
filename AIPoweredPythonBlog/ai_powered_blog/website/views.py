from django.shortcuts import render

from posts.models import Post
from posts.selectors import get_sidebar_categories


def home(request):
    latest_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-published_at")[:6]
    )

    categories = get_sidebar_categories()

    context = {
        "latest_posts": latest_posts,
        "categories": categories,
    }
    return render(request, "website/home.html", context)


def about(request):
    categories = get_sidebar_categories()

    context = {
        "categories": categories,
    }
    return render(request, "website/about.html", context)
