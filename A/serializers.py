from rest_framework import serializers
from .models import add_post
from comment.models import comment
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

class CommentSerializer(ModelSerializer):
    comment_related_user = serializers.StringRelatedField()
    class Meta:
        model = comment
        fields = ("id", "comment_related_user", "comment_text", "comment_date", "comment_edition_date")
        #read_only_fields = ("post_edition_date", "post_publication_date", "post_related_user")

class AddPostSerializer(ModelSerializer):
    #post_related_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), )
    post_related_user = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = add_post
        fields = ("id", "post_title", "post_related_user", "post_text",
                  "post_edition_date", "post_publication_date",
                  "post_image", "comments") #("post_title", )
        read_only_fields = ("post_edition_date", "post_publication_date", "post_related_user",)





#print(repr(a))
# class UserSerializer(ModelSerializer):
#     user_related_posts =
#     class Meta:
#         model = User
#         fields = "__all__" #("post_title", )
