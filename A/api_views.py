from .serializers import AddPostSerializer #UserSerializer
from .models import add_post
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, BasePermission

class StaffCUDonlyOrUserWhoCreated(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """Check if question related user id is the same as request.user.id"""
        current_user = request.user
        if current_user.is_staff or request.method == "GET":
            return True
        else:
            question_user_id = obj.post_related_user.id
            return current_user.id == question_user_id


class AddPostListApi(ModelViewSet):
    queryset = add_post.objects.all()
    serializer_class = AddPostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, StaffCUDonlyOrUserWhoCreated)

    def perform_create(self, serializer):
        """Link User to created question"""
        serializer.save(post_related_user=self.request.user)
