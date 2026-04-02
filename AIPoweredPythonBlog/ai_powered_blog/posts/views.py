from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from tags.models import Tag
from .models import Post


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


def post_list(request):
    category_slug = request.GET.get('category')

    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related('author')
        .prefetch_related('tags')
        .order_by('-published_at')
    )

    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Tag, slug=category_slug)
        posts = posts.filter(tags__slug=category_slug).distinct()

    context = {
        'posts': posts,
        'categories': get_categories(),
        'selected_category': selected_category,
    }
    return render(request, 'posts/list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('tags'),
        slug=slug,
        status=Post.Status.PUBLISHED
    )

    related_posts = (
        Post.objects.filter(
            status=Post.Status.PUBLISHED,
            tags__in=post.tags.all()
        )
        .exclude(id=post.id)
        .select_related('author')
        .prefetch_related('tags')
        .distinct()
        .order_by('-published_at')[:3]
    )

    context = {
        'post': post,
        'related_posts': related_posts,
        'categories': get_categories(),
    }
    return render(request, 'posts/detail.html', context)
