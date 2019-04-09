from rest_framework import serializers
from .models import add_post
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

class AddPostSerializer(ModelSerializer):
    class Meta:
        model = add_post
        fields = "__all__"#("post_title", )

# class UserSerializer(ModelSerializer):
#     user_related_posts =
#     class Meta:
#         model = User
#         fields = "__all__" #("post_title", )
