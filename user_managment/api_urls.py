from django.urls import path, include
from . import api_views
from rest_framework import routers

CRUDUser = routers.SimpleRouter()
CRUDUser.register("", api_views.CRUDUserAPI)

urlpatterns = [
    path("", include(CRUDUser.urls)),

]
