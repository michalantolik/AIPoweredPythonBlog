from django.contrib import admin

from posts.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("sort_order", "name", "slug")
    ordering = ("sort_order", "name")
    search_fields = ("name", "slug")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "author", "published_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "slug", "excerpt", "content", "author__username", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
