from django.db.models import Count, Q
from django.shortcuts import render

from posts.models import Post
from tags.models import Tag


def get_categories():
    return (
        Tag.objects.annotate(
            published_posts_count=Count(
                'posts',
                filter=Q(posts__status=Post.Status.PUBLISHED),
                distinct=True
            )
        )
        .filter(published_posts_count__gt=0)
        .order_by('name')
    )


def home(request):
    latest_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related('author')
        .prefetch_related('tags')
        .order_by('-published_at')[:6]
    )

    categories = get_categories()

    context = {
        'latest_posts': latest_posts,
        'categories': categories,
    }
    return render(request, 'website/home.html', context)


def about(request):
    categories = get_categories()

    context = {
        'categories': categories,
    }
    return render(request, 'website/about.html', context)