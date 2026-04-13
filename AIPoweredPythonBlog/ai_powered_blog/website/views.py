from django.core.paginator import Paginator
from django.shortcuts import render
from wagtail.models import Site

from cms.models import BlogIndexPage


POSTS_PER_PAGE = 6


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


def _build_query_string(request, **updates):
    query_params = request.GET.copy()
    query_params.pop("page", None)

    for key, value in updates.items():
        if value in (None, ""):
            query_params.pop(key, None)
        else:
            query_params[key] = value

    return query_params.urlencode()


def home(request):
    blog_index = _get_blog_index_for_request(request)
    blog_index_url = _get_blog_index_url(blog_index)

    if blog_index is None:
        context = {
            "latest_posts": [],
            "categories": [],
            "selected_category": None,
            "sidebar_base_url": "/",
            "blog_index_url": blog_index_url,
            "pagination_query_string": "",
            "page_obj": None,
            "all_posts_query_string": "",
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

    paginator = Paginator(latest_posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "latest_posts": page_obj.object_list,
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "sidebar_base_url": "/",
        "blog_index_url": blog_index_url,
        "pagination_query_string": _build_query_string(request),
        "all_posts_query_string": _build_query_string(request, category=""),
    }
    return render(request, "website/home.html", context)


def about(request):
    blog_index = _get_blog_index_for_request(request)
    blog_index_url = _get_blog_index_url(blog_index)

    context = {
        "categories": blog_index.get_sidebar_categories() if blog_index else [],
        "selected_category": None,
        "sidebar_base_url": blog_index_url,
        "blog_index_url": blog_index_url,
    }
    return render(request, "website/about.html", context)
