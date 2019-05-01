from .serializers import AddPostSerializer, CommentSerializer #UserSerializer
from .models import add_post
from comment.models import comment
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, BasePermission
from rest_framework.decorators import action

class StaffCUDonlyOrUserWhoCreated(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """Check if question or comment related user id is the same as request.user.id"""
        current_user = request.user
        if current_user.is_staff or request.method == "GET":
            return True
        else:
            if isinstance(view, CommentUpdateDelete):
                comment_user_id = obj.comment_related_user
                return current_user == comment_user_id
            else: # same as isinstance(view, AddPostListApi):
                question_user_id = obj.post_related_user.id
                return current_user.id == question_user_id



class AddPostListApi(ModelViewSet):
    queryset = add_post.objects.all()
    serializer_class = AddPostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, StaffCUDonlyOrUserWhoCreated)

    def perform_create(self, serializer):
        """Link User to created question"""
        serializer.save(post_related_user=self.request.user)

    @action(detail=True, methods=["get", "post",], url_path="comments")
    def PostComments(self, request, pk=None, comment_id=None):
        """Action for retrieving comments related
        to particular question or to creatin new one."""
        question = self.get_object()
        queryset = question.comments.all()
        serializer_class = CommentSerializer
        data = request.data
        if request.method == "GET":
            if len(queryset) == 0:
                return Response({"Comments": "No comments"})
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            print("DDA:", data)
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(comment_related_user=request.user, related_post=question)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentUpdateDelete(RetrieveUpdateDestroyAPIView):  #(DestroyModelMixin, UpdateAPIView):
    queryset = comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, StaffCUDonlyOrUserWhoCreated)
    lookup_url_kwarg = "comment_id"
    
    def get_object(self):
        """Idea is to get only comments related to some questions:
            url: questions/<pk>/comments/<comment_id>
            If question <pk> does not exist --> 404
            If question <pk> do not have related comment with <comment_id> --> 404
            Smth. like this..."""
        questions = add_post.objects.all()
        question_id = self.kwargs["pk"]
        comment_id = self.kwargs["comment_id"]
        question = get_object_or_404(questions, id=question_id) #if question exists with pk
        related_comments = question.comments.all() # backward relation queryset
        comment_related_to_question = get_object_or_404(related_comments, id=comment_id)
        return super().get_object()
        # @action(detail=True, methods=["put", "delete"],)
        # def CommentPutDel(self, request, pk=None, comment_id=None):
        #     if request.method == "PUT":
        #         comment_instance = queryset.get(id=comment_id)
        #         serializer = CommentSerializer(comment_instance, data=data, partial=False)
        #         serializer.is_valid(raise_exception=True)
        #         serializer.save()
        #         return Response(serializer.data)
        #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
