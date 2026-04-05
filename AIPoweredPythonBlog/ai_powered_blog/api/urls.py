from django.urls import path

from .views import post_detail_api, post_list_api, tag_list_api

app_name = 'api'

urlpatterns = [
    path('posts/', post_list_api, name='post-list'),
    path('posts/<slug:slug>/', post_detail_api, name='post-detail'),
    path('tags/', tag_list_api, name='tag-list'),
]
