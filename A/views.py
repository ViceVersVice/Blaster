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
def PrivacyPolicyView(request):
    return render(request, "privacy_policy.html")

def AboutView(request):
    """Simple about page view"""
    return render(request, "about.html")

def custom_pagination(context):
    """In pagiantion shows only 7 (3 previous/1 current/3 next) pages with current page in middle"""
    page_obj = context["page_obj"] # gets page object
    page_num = page_obj.number # gets current page number
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
    #return namedtuple("start_end", [start, end])
    context["iter"] = page_obj.paginator.page_range[start:end]
    return context

class homeTestView(ListView, FormView):
    """Questions and answears view. Show question list (ListView)
    and operates question form (FormView).

    Attributes:
        queryset: post(question) objects queryset
        form_class: corresponding form_class
        success_url: url to redirect after successful form validation
        context_object_name: custom template tag for add_post queryset
        paginate_by: defines how many posts are seen per page
        template_name: html template
    """

    queryset = add_post.objects.all()
    form_class = post_form
    success_url = reverse_lazy("homeT")
    context_object_name = "postlist"
    paginate_by = 3
    template_name = "home1.html"
    def get_user(self):
        """Gets current user"""
        usr = self.request.user
        return usr

    def get_context_data(self, **kwargs):
        """Adds additional context data, defines custom pagination"""
        context = super().get_context_data(**kwargs)
        try:
            if self.request.session["Activation"] == True: # this will be shown only after sending activation email
                context["Activation"] = True
                self.request.session["Activation"] = False
        except:
            pass
        context = custom_pagination(context) # adds custom pagination
        return context

    def form_valid(self, form):
        """Savesquestion, saves also user related with this question """
        k = form.save(commit=False)
        k.post_related_user = self.get_user()
        k.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object_list = self.get_queryset() # redefines demanded object_list for ListView
        return super().form_invalid(form)

class postView(ListView, BaseCreateView):
    """Question and it`s comments view. Show question, comments list and
    processes comment form

    Attributes:
        template_name: html templates name
        pk_url_kwarg: id (pk) of current question
        form_class: comment form class
        context_object_name: custom name of comment objects
        paginate_by: defines how many comments are seen per page
    """
    #queryset = add_post.objects.all()
    template_name = "post.html"
    pk_url_kwarg = "post_id"
    form_class = comment_form
    context_object_name = "post_comments"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Adds additional context data, defines custom pagination"""
        context = super().get_context_data(**kwargs)
        context = custom_pagination(context) # adds custom pagination
        return context

    def form_invalid(self, form):
        """"""
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return super().form_invalid(form)

    def get_user(self):
        """Returns current user"""
        usr = self.request.user
        return usr

    def get_object(self):
        """Gets post object (some question)"""
        return super().get_object(queryset=add_post.objects.all())

    def get_success_url(self, **kwargs):
        """Return url to the same post (question)"""
        return reverse_lazy("post1", kwargs={'post_id': self.get_object().id})

    def get(self, request, *args, **kwargs):
        """Adds object like in BaseCreateView needed to get_context_data"""
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Saves form with comment"""
        k = form.save(commit=False)
        k.related_post = self.get_object() # comment related post
        k.comment_related_user = self.get_user() # comment related user
        k.save()
        return super().form_valid(form)

    def get_queryset(self):
        """Returns post related comments queryset"""
        return self.get_object().comments.all()

class DeletePost(UserPassesTestMixin, DeleteView):
    """View for deleting posts (questions)

    Attributes: add_post objects queryset
    pk_url_kwarg: id of post (question) in url"""

    queryset = add_post.objects.all()
    pk_url_kwarg = "num"
    def get(self, request, *args, **kwargs):
        """Skipped rendering template step"""
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):
        "Returns url to question list"
        return reverse("homeT")
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        """Allowes deleting only for users which had created this questions"""
        current_user = self.request.user
        post_user = self.get_object().post_related_user
        if current_user == post_user:
            return True
        else:
            return False

class EditPost(UserPassesTestMixin, UpdateView):
    """View for editing posts (questions)

    Attributes:
        .....same...
    """

    queryset = add_post.objects.all()
    pk_url_kwarg = "num"
    template_name = "edit_post.html"
    form_class = post_form
    def get_success_url(self):
        """Returns url to edited post (question)"""
        return reverse_lazy("post1", kwargs={'post_id': self.get_object().id})
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        """Allowes deleting only for users which had created this questions"""
        current_user = self.request.user
        post_user = self.get_object().post_related_user
        if current_user == post_user:
            return True
        else:
            return False
