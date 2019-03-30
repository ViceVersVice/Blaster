from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.views.generic import RedirectView
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.edit import CreateView, ModelFormMixin, BaseCreateView, CreateView, FormView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout, authenticate, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import edit_user_profile_form, RegisterForm, PasswordResetForm2
from A.models import add_post
from .models import user_profile
from comment.models import comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponseForbidden
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    #changed user.password to user.is_active, due to password hash change every time it is called
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)

class PasswordResetView2(PasswordResetView):
    form_class = PasswordResetForm2

class PasswordResetConfirmView2(PasswordResetConfirmView):
    success_url = reverse_lazy("sign_in")
    def form_valid(self, form):
        self.request.session["reset_complete"] = True
        return super().form_valid(form)

class PasswordChangeView2(PasswordChangeView):
    def get_success_url(self):
        print(self.request.user.id)
        #return reverse_lazy("homeT")
        return reverse_lazy("current_user_profile", kwargs={"user_id": int(self.request.user.id)})




class UserProfile(DetailView):
    queryset = User.objects.all()
    pk_url_kwarg = "user_id"
    template_name = "user_profile.html"
    success_url = reverse_lazy("homeT")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context



class UserRegister(UserPassesTestMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = "user_register.html"
    success_url = reverse_lazy("homeT")
    def form_valid(self, form):
        self.request.session["Activation"] = True
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        u_id = urlsafe_base64_encode(force_bytes(self.object.id))
        u_id_string = u_id.decode("utf-8")
        token_generator_class = AccountActivationTokenGenerator()
        token = token_generator_class.make_token(self.object)
        link = "{0}".format(reverse_lazy("activation", kwargs={"u_id": "{0}".format(u_id_string), "token": "{0}".format(token), }))
        message = render_to_string("user_activation_message.html", {"user": self.object, "link": link})
        #activation_message = EmailMessage()
        try:
            send_mail("Blaster acc activation",
            "Welcome to future!",
            'blaster.inf.tool@gmail.com',
            [form.cleaned_data["email"]],
            fail_silently=False, html_message=message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        # username, password = form.cleaned_data["username"], form.cleaned_data["password1"]
        # auth_user = authenticate(username=username, password=password)
        # login_user = login(self.request, auth_user)
        new_user_profile = user_profile(profile_related_user=self.object)
        new_user_profile.save()
        return super().form_valid(form)
    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        else:
            return True

def activate_user(request, u_id, token):
    token_generator_class = AccountActivationTokenGenerator()
    decoded_id = force_text(urlsafe_base64_decode(u_id))
    user_obj = User.objects.get(id=decoded_id)
    token_check = token_generator_class.check_token(user_obj, token)
    print(token_check)
    if user_obj is not None and token_check:
        user_obj.is_active = True
        user_obj.save()
        login(request, user_obj)
        return HttpResponseRedirect(reverse_lazy("edit_current_user_profile",
        kwargs={'user_id': user_obj.id}))
    else:
        return HttpResponse("Activation link is invalid!!")

class EditUserProfile(UserPassesTestMixin, UpdateView):
    queryset = User.objects.all()
    pk_url_kwarg = "user_id"
    form_class = edit_user_profile_form
    template_name = "edit_user_profile.html"
    def get_object(self, queryset=None):
        user_obj = super().get_object()
        obj = user_obj.user_profile
        return obj
    def get_success_url(self):
        user_id = self.get_object().profile_related_user.id
        #user_id = user_profile.profile_related_user.id
        #print("USER_ID", user)
        return reverse_lazy("current_user_profile",
        kwargs={'user_id': user_id})

    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        user = self.request.user
        user_post = super().get_object()
        if user == user_post:
            return True
        else:
            return False

class Logout(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)
    pattern_name = "homeT"

class Sign_in(UserPassesTestMixin, LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["reset_complete"] = self.request.session["reset_complete"]
            self.request.session["reset_complete"] = False
        except:
            pass
        return context
    def form_valid(self, form):
        login(self.request, form.get_user())
        user_id = self.request.user.id
        # update last_activity after login
        user_profile.objects.filter(profile_related_user=user_id).update(last_activity=timezone.now())
        return HttpResponseRedirect(reverse("about"))

    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        else:
            return True
