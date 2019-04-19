from rest_framework import serializers
from .models import add_post
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

class AddPostSerializer(ModelSerializer):
    #post_related_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), )
    post_related_user = serializers.StringRelatedField()
    class Meta:
        model = add_post
        fields = "__all__"#("post_title", )
        read_only_fields = ("post_edition_date", "post_publication_date", "post_related_user")
a = AddPostSerializer()
#print(repr(a))
# class UserSerializer(ModelSerializer):
#     user_related_posts =
#     class Meta:
#         model = User
#         fields = "__all__" #("post_title", )
