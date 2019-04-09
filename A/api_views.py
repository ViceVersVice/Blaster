from .serializers import AddPostSerializer #UserSerializer
from .models import add_post
from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView

class AddPostListApi(ListAPIView):
    queryset = add_post.objects.all()
    serializer_class = AddPostSerializer

# class UserListApi(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
