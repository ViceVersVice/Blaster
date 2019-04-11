from django.urls import path
from . import api_views


urlpatterns = [
    path("user-auth/", api_views.UserAuthApiView.as_view(), name="user_auth_api"),

]
