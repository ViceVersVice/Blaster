from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .serializers import RepresentationUserAPISerializer, CreateUserAPISerializerAndPasswordConfirm
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .models import user_profile
class AllowAnyPOST_GET(BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return True
        # if request.user.is_staff or request.method == "GET":
        #     return True
        # else:
        #     return request.user.id == obj.id


class CRUDUserAPI(ModelViewSet):
    """Operates create, retrieve, update, partial update and list, retrieve of
    User object. Password confirmation is needed for POST, PUT, PATCH.
    """
    serializer_class = RepresentationUserAPISerializer
    queryset = User.objects.all()
    permission_classes = (AllowAnyPOST_GET,)

    def get_serializer_class(self):
        specified_actions = ["list", "retrieve",]
        if self.action in specified_actions:
            return self.serializer_class
        else:
            return CreateUserAPISerializerAndPasswordConfirm

    def perform_create(self, serializer):
        print(serializer.instance)
        serializer.save()
        user_profile.objects.create(profile_related_user=serializer.instance) # creates user profile

    # @action(detail=False, methods=['post'])
    # def LoginAUTH(self, request):
