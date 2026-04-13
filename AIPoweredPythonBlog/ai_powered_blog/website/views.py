from django.shortcuts import render
from wagtail.models import Site

from cms.models import BlogIndexPage


def _get_blog_index_for_request(request):
    site = (
        Site.find_for_request(request)
        or Site.objects.filter(is_default_site=True).first()
        or Site.objects.first()
    )

    if site is None:
        return None

    return (
        BlogIndexPage.objects.child_of(site.root_page)
        .live()
        .public()
        .first()
    )


def _get_blog_index_url(blog_index):
    return blog_index.url if blog_index else "/articles/"


def home(request):
    blog_index = _get_blog_index_for_request(request)
    blog_index_url = _get_blog_index_url(blog_index)

    if blog_index is None:
        context = {
            "latest_posts": [],
            "categories": [],
            "selected_category": None,
            "sidebar_base_url": request.path,
            "blog_index_url": blog_index_url,
        }
        return render(request, "website/home.html", context)

    category_slug = request.GET.get("category", "").strip()
    categories = blog_index.get_sidebar_categories()
    selected_category = None

    latest_posts = blog_index.get_posts_queryset()

    if category_slug:
        selected_category = categories.filter(slug=category_slug).first()
        if selected_category:
            latest_posts = latest_posts.filter(category=selected_category)

    latest_posts = latest_posts[:6]

    context = {
        "latest_posts": latest_posts,
        "categories": categories,
        "selected_category": selected_category,
        "sidebar_base_url": request.path,
        "blog_index_url": blog_index_url,
    }
    return render(request, "website/home.html", context)


def about(request):
    blog_index = _get_blog_index_for_request(request)
    blog_index_url = _get_blog_index_url(blog_index)

    context = {
        "categories": blog_index.get_sidebar_categories() if blog_index else [],
        "selected_category": None,
        "sidebar_base_url": "/",
        "blog_index_url": blog_index_url,
    }
    return render(request, "website/about.html", context)
