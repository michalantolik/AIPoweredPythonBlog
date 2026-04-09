from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


def populate_blog_post_relations(apps, schema_editor):
    BlogPostPage = apps.get_model("cms", "BlogPostPage")
    Category = apps.get_model("posts", "Category")
    Tag = apps.get_model("tags", "Tag")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Page = apps.get_model("wagtailcore", "Page")

    first_user = User.objects.order_by("id").first()
    if first_user is None:
        raise RuntimeError(
            "Cannot migrate BlogPostPage.author because no users exist. "
            "Create at least one user before running this migration."
        )

    max_sort_order = Category.objects.order_by("-sort_order").values_list("sort_order", flat=True).first() or 0

    default_category, _ = Category.objects.get_or_create(
        slug="uncategorized",
        defaults={
            "name": "Uncategorized",
            "sort_order": max_sort_order + 1,
        },
    )

    default_tag, _ = Tag.objects.get_or_create(
        slug="general",
        defaults={
            "name": "General",
        },
    )

    through_model = BlogPostPage.tags.through

    for blog_post in BlogPostPage.objects.all():
        owner_id = (
            Page.objects.filter(id=blog_post.page_ptr_id)
            .values_list("owner_id", flat=True)
            .first()
        )

        blog_post.author_id = owner_id or first_user.id
        blog_post.category_id = default_category.id
        blog_post.save(update_fields=["author", "category"])

        if not through_model.objects.filter(blogpostpage_id=blog_post.pk).exists():
            through_model.objects.create(
                blogpostpage_id=blog_post.pk,
                tag_id=default_tag.id,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0001_initial"),
        ("posts", "0003_category_alter_post_tags_post_category"),
        ("tags", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogpostpage",
            name="cover_image",
        ),
        migrations.RemoveField(
            model_name="blogpostpage",
            name="published_on",
        ),
        migrations.RemoveField(
            model_name="blogpostpage",
            name="topic",
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to="posts.category",
            ),
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="tags",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True,
                related_name="blog_posts",
                to="tags.tag",
            ),
        ),
        migrations.RunPython(
            populate_blog_post_relations,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="blogpostpage",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="blogpostpage",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to="posts.category",
            ),
        ),
        migrations.AlterField(
            model_name="blogpostpage",
            name="tags",
            field=modelcluster.fields.ParentalManyToManyField(
                related_name="blog_posts",
                to="tags.tag",
            ),
        ),
    ]
