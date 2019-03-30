from django.urls import path
from . import views


urlpatterns = [
    path("tool/", views.Blaster.as_view(), name="blaster"),
    path("tool/<slug:output_id>", views.Blaster.as_view(), name="blaster"),
    path("tool/<slug:output_id>/download", views.download_file, name="download_file")
    #path("post/id=<int:num>/delcom1/id<int:id>/", views.DeleteComment.as_view(), name="delcom1"),


    #path('', views.index, name='index'),
]
