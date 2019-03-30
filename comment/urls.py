from django.urls import path
from . import views


urlpatterns = [
    #path("post/<int:num>/delcom/id<int:id>/", views.del_comm, name="delcom"),
    path("post/id=<int:post_id>/delcom1/id<int:comment_id>/", views.DeleteComment.as_view(), name="delcom1"),
    #path("post/id=<int:post_id>/delcom1/id<int:comment_id>/", views.DeleteComment.as_view(), name="delcom1"),


    #path('', views.index, name='index'),
]
