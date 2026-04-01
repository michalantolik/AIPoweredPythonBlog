from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-published_at')
    return render(request, 'posts/list.html', {'posts': posts})


def post_detail(request, slug):
    return render(request, 'posts/detail.html', {'slug': slug})
