from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.core import serializers
from django.views.generic.list import ListView, BaseListView
from django.views.generic.edit import CreateView, ModelFormMixin, BaseCreateView, CreateView, FormView, UpdateView, BaseUpdateView, DeleteView, DeletionMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.views.generic import View
from .forms import post_form
from comment.forms import comment_form
from .models import add_post
from comment.models import comment
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.http import HttpResponseForbidden

######################################################
#About page and How # TO:
def AboutView(request):
    return render(request, "about.html")


class homeTestView(ListView, FormView):
    queryset = add_post.objects.all()
    form_class = post_form
    success_url = ""
    context_object_name = "postlist"
    paginate_by = 3
    template_name = "home1.html"
    def get_user(self):
        usr = self.request.user
        return usr

    def get_success_url(self):
        return reverse("homeT")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session["Activation"] == True:
                context["Activation"] = True
                self.request.session["Activation"] = False
        except:
            pass
        page_obj = context["page_obj"]
        page_num = page_obj.number
        if (page_num - 4) <= 0:
            start = 0
            end = 6
        elif (page_obj.paginator.num_pages - page_num) < 4:
            start = page_obj.paginator.num_pages - 7
            if start < 0:
                start = 0
            end = page_obj.paginator.num_pages
        else:
            start = page_num - 4
            end = page_num + 3
        context["iter"] = page_obj.paginator.page_range[start:end]
        return context

    def form_valid(self, form):
        k = form.save(commit=False)
        k.post_related_user = self.get_user()
        k.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return super().form_invalid(form)

class postView(ListView, BaseCreateView):
    template_name = "post.html"
    pk_url_kwarg = "post_id"
    form_class = comment_form
    context_object_name = "post_comments"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context["page_obj"]
        page_num = page_obj.number
        if (page_num - 4) <= 0:
            start = 0
            end = 6
        elif (page_obj.paginator.num_pages - page_num) < 4:
            start = page_obj.paginator.num_pages - 7
            if start < 0:
                start = 0
            end = page_obj.paginator.num_pages
        else:
            start = page_num - 4
            end = page_num + 3
        context["iter"] = page_obj.paginator.page_range[start:end]
        print(page_obj.paginator.page_range[start:end])
        return context

    def form_invalid(self, form):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return super().form_invalid(form)

    def get_user(self):
        usr = self.request.user
        return usr

    def get_object(self):
        return super().get_object(queryset=add_post.objects.all())

    def get_success_url(self, **kwargs):
        return reverse_lazy("post1", kwargs={'post_id': self.get_object().id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
         k = form.save(commit=False)
         k.related_post = self.get_object()
         k.comment_related_user = self.get_user()
         k.save()
         return super().form_valid(form)

    def get_queryset(self):
        return self.get_object().comment_set.all()

class DeletePost(UserPassesTestMixin, DeleteView):
    queryset = add_post.objects.all()
    pk_url_kwarg = "num"
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):
        return reverse("homeT")
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        current_user = self.request.user
        post_user = self.get_object().post_related_user
        if current_user == post_user:
            return True
        else:
            return False

class EditPost(UserPassesTestMixin, UpdateView):
    queryset = add_post.objects.all()
    pk_url_kwarg = "num"
    template_name = "edit_post.html"
    form_class = post_form
    def get_success_url(self):
        return reverse_lazy("post1", kwargs={'post_id': self.get_object().id})
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        current_user = self.request.user
        post_user = self.get_object().post_related_user
        if current_user == post_user:
            return True
        else:
            return False
