from rest_framework import serializers
from .models import user_profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RepresentationUserAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True},
                        "id": {"read_only": True},
                        "email": {"required": True}
                        }
        #read_only_fields = ("id_num",)
class CreateUserAPISerializerAndPasswordConfirm(RepresentationUserAPISerializer):
    """Adds non model field confirm_password for consequent passwords comparing.
    Username and email are unchangeable (for now) after being created (for PUT, PATCH).
    """
    confirm_password = serializers.CharField(max_length=128, required=True, write_only=True)
    class Meta(RepresentationUserAPISerializer.Meta):
        fields = RepresentationUserAPISerializer.Meta.fields + ("confirm_password", )
        extra_kwargs = RepresentationUserAPISerializer.Meta.extra_kwargs
        #extra_kwargs["username"] = {'read_only': True}

    def validate(self, data):
        if data.get("password", None) == None or data.get("confirm_password", None) == None: #only for PATCH
            raise serializers.ValidationError("Password required")
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords are not equal!")
        """Excludes confirm_password before create/update/partial_update User model instance"""
        del data["confirm_password"]
        data["password"] = make_password(data["password"]) #makes hashed password before create/update/partial_update
        return data

    def get_fields(self):
        fields = super().get_fields()
        """Username is unchangeable after User beign created"""
        if self.context.get("request").method != "POST":
            fields["username"].read_only = True
            fields["email"].read_only = True
        return fields
