from posts.models import Category, Post
from tags.models import Tag


def serialize_category(category: Category) -> dict:
    return {
        "name": category.name,
        "slug": category.slug,
    }


def serialize_tag(tag: Tag) -> dict:
    return {
        "name": tag.name,
        "slug": tag.slug,
    }


def serialize_post_summary(post: Post) -> dict:
    return {
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt,
        "status": post.status,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "author": {
            "username": post.author.username,
        },
        "category": serialize_category(post.category),
        "tags": [serialize_tag(tag) for tag in post.tags.all()],
        "detail_url": f"/api/posts/{post.slug}/",
        "web_url": f"/articles/{post.slug}/",
    }


def serialize_post_detail(post: Post) -> dict:
    payload = serialize_post_summary(post)
    payload["content"] = post.content
    return payload
