from django.urls import path, include
from rest_framework import routers
#from rest_framework_nested import routers as NestedRouters
from . import views, api_views


question_router = routers.SimpleRouter()
question_router.register("", api_views.AddPostListApi)

# question_routerPut_delete = NestedRouters.NestedSimpleRouter(question_router, "", lookup='comment')
# question_routerPut_delete.register("", api_views.AddPostListApi)
for i in question_router.urls:
    print(i)

"""API urls"""
urlpatterns = [
    path("", include(question_router.urls)),
    path("<int:pk>/comments/<int:comment_id>/", api_views.CommentUpdateDelete.as_view(), name="comments_api"),
    #path("", include(question_routerPut_delete.urls)),
    #path("posts-list/", api_views.AddPostListApi.as_view(), name="posts_list"),
    #path("users-list/", api_views.UserListApi.as_view(), name="users_list"),
]
