from django.urls import path, include
from rest_framework import routers
from . import views, api_views


question_router = routers.SimpleRouter()
question_router.register("", api_views.AddPostListApi)
print(question_router.urls)
"""API urls"""
urlpatterns = [
    path("", include(question_router.urls)),
    #path("posts-list/", api_views.AddPostListApi.as_view(), name="posts_list"),
    #path("users-list/", api_views.UserListApi.as_view(), name="users_list"),
]
