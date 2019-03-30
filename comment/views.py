from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.core import serializers
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.edit import CreateView, ModelFormMixin, BaseCreateView, CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from .forms import comment_form
from A.models import add_post
from comment.models import comment
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.http import HttpResponseForbidden
# Create your views here.

class EditComment(UserPassesTestMixin, UpdateView):
    queryset = comment.objects.all()
    pk_url_kwarg = "comment_id"
    def get_success_url(self):
        post_id = self.kwargs["post_id"]
        return reverse_lazy("post1", kwargs={'post_id': post_id})
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        current_user = self.request.user
        comment_user = self.get_object().comment_related_user
        if current_user == comment_user:
            return True
        else:
            return False

class DeleteComment(UserPassesTestMixin, DeleteView):
    queryset = comment.objects.all()
    pk_url_kwarg = "comment_id"
    def get_success_url(self):
        post_id = self.kwargs["post_id"]
        return reverse_lazy("post1", kwargs={'post_id': post_id})
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        current_user = self.request.user
        comment_user = self.get_object().comment_related_user
        if current_user == comment_user:
            return True
        else:
            return False



# def del_comm(request, num, id):
#     if request.method == 'POST':
#         a = comment.objects.get(id=id)
#         a.delete()
#         return redirect(reverse("post1", kwargs={'post_id': num}))
#     else:
#         redirect("http://127.0.0.1:8000/App/post/%s" % num)
