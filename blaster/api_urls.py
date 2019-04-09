from django.urls import path
from . import api_views


urlpatterns = [
    path("io/", api_views.BlasterIOApiView.as_view(), name="blaster_io_api"),

]
