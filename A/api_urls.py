from django.urls import path

from . import views, api_views


"""API urls"""
urlpatterns = [

    path("posts-list/", api_views.AddPostListApi.as_view(), name="posts_list"),
    #path("users-list/", api_views.UserListApi.as_view(), name="users_list"),
]
