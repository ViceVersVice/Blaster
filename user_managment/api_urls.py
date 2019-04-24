from django.urls import path, include
from . import api_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

CRUDUser = routers.SimpleRouter()
CRUDUser.register("", api_views.CRUDUserAPI)

urlpatterns = [
    path("crud/", include(CRUDUser.urls)),
    path("token-auth/", obtain_auth_token),

]
