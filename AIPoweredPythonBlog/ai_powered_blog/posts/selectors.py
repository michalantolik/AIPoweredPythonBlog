from django.db.models import Count, Q

from posts.models import Category, Post


def get_sidebar_categories():
    return (
        Category.objects.annotate(
            published_posts_count=Count(
                "posts",
                filter=Q(posts__status=Post.Status.PUBLISHED),
                distinct=True,
            )
        )
        .filter(published_posts_count__gt=0)
        .order_by("sort_order", "name")
    )
