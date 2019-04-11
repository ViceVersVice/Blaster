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
from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Class used to generate unique password reset token for account activation
    and password reset"""

    def _make_hash_value(self, user, timestamp):
        """See django.contrib.auth.tokens source code. Changed user.password value to user.is_active,
         due to password hash changes every time it is called"""
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)

class PasswordResetView2(PasswordResetView):
    """View for password reset"""
    form_class = PasswordResetForm2

class PasswordResetConfirmView2(PasswordResetConfirmView):
    """View for password reset confirmation after successful password reset

    Attributes:
        success_url: login page url
    """

    success_url = reverse_lazy("sign_in")
    def form_valid(self, form):
        """After successful form validation redirects to success url"""
        self.request.session["reset_complete"] = True # value needed to show message in html after successful password reset
        return super().form_valid(form)

class PasswordChangeView2(PasswordChangeView):
    """View for password change"""
    def get_success_url(self):
        """Provides url after successful password change"""
        #print(self.request.user.id)
        return reverse_lazy("current_user_profile", kwargs={"user_id": int(self.request.user.id)})




class UserProfile(DetailView):
    """View for user profile representation

    Attributes:
        queryset: User object get_queryset
        pk_url_kwarg: pk (id) of user
        template_name: html template name
    """

    queryset = User.objects.all()
    pk_url_kwarg = "user_id"
    template_name = "user_profile.html"
    def get_context_data(self, **kwargs):
        """Adds to context current user"""
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context



class UserRegister(UserPassesTestMixin, CreateView):
    """View for user Registration. Handles activation mail sending.

    Attributes:
        model: User model
        form_class: registration form class
        template_name: html template name
        success_url: url after successful registration
    """

    model = User
    form_class = RegisterForm
    template_name = "user_register.html"
    success_url = reverse_lazy("homeT")
    def form_valid(self, form):
        """After successful form validation generates unique activation link,
        sends activation mail, creates user_profile for new user.
        """
        self.request.session["Activation"] = True # value needed for message
        self.object = form.save(commit=False)
        self.object.is_active = False # new user is in inactive state
        self.object.save() # save User object
        u_id = urlsafe_base64_encode(force_bytes(self.object.id)) # encodes unique uuid based on user id
        u_id_string = u_id.decode("utf-8") # decoded uuid value for url
        token_generator_class = AccountActivationTokenGenerator()
        token = token_generator_class.make_token(self.object)
        token_link_part = reverse_lazy("activation", kwargs={"u_id": "{0}".format(u_id_string), "token": "{0}".format(token), })
        domain = settings.ALLOWED_HOSTS[0] # creates unique one time usable token
        link = "https://{0}/{1}".format(domain, token_link_part)
        message = render_to_string("user_activation_message.html", {"user": self.object, "link": link}) # rendered message with activation link
        #activation_message = EmailMessage()
        try:
            # Sends activation message
            send_mail("Blaster acc activation",
            "Welcome to future!",
            'blaster.inf.tool@gmail.com',
            [form.cleaned_data["email"]],
            fail_silently=False, html_message=message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        new_user_profile = user_profile(profile_related_user=self.object) # creates profile for User object
        new_user_profile.save()
        return super().form_valid(form)
    def handle_no_permission(self):
        return HttpResponseForbidden()

    def test_func(self):
        """Test function to prevent logged users to acces to this view"""
        user = self.request.user
        if user.is_authenticated:
            return False
        else:
            return True

def activate_user(request, u_id, token):
    """Validates activation token in activation link"""
    token_generator_class = AccountActivationTokenGenerator()
    decoded_id = force_text(urlsafe_base64_decode(u_id))
    user_obj = User.objects.get(id=decoded_id)
    token_check = token_generator_class.check_token(user_obj, token)
    #print(token_check)
    if user_obj is not None and token_check:
        user_obj.is_active = True # activates user
        user_obj.save()
        login(request, user_obj) # user autologin after activation
        return HttpResponseRedirect(reverse_lazy("edit_current_user_profile",
                                                 kwargs={'user_id': user_obj.id}))
    else:
        return HttpResponse("Activation link is invalid!!")

class EditUserProfile(UserPassesTestMixin, UpdateView):
    """View for user profile editing

    Attributes:
        queryset: User object
        pk_url_kwarg: User obejct id (pk)
        form_class: edit user profile form class
        template_name: html template name
        success_url: url after successful editing
    """

    queryset = User.objects.all()
    pk_url_kwarg = "user_id"
    form_class = edit_user_profile_form
    template_name = "edit_user_profile.html"
    def get_object(self, queryset=None):
        """Returns User related user_profile object"""
        user_obj = super().get_object()
        obj = user_obj.user_profile
        return obj
    def get_success_url(self):
        """Returns url to user_profile view"""
        user_id = self.get_object().profile_related_user.id
        return reverse_lazy("current_user_profile", kwargs={'user_id': user_id})

    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        """Prevents another users to edit this profile"""
        user = self.request.user
        user_post = super().get_object()
        if user == user_post:
            return True
        else:
            return False

class Logout(RedirectView):
    """Logout user"""
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super().get(request, *args, **kwargs)
    pattern_name = "homeT"

class Sign_in(UserPassesTestMixin, LoginView):
    """Sign in view"""
    def get_context_data(self, **kwargs):
        """Adds additional context after password reset"""
        context = super().get_context_data(**kwargs)
        try:
            context["reset_complete"] = self.request.session["reset_complete"]
            self.request.session["reset_complete"] = False
        except:
            pass
        return context
    def form_valid(self, form):
        """After successful login form validation, logins user, updates user last_activity"""
        login(self.request, form.get_user())
        user_id = self.request.user.id
        # update last_activity after login
        user_profile.objects.filter(profile_related_user=user_id).update(last_activity=timezone.now())
        return HttpResponseRedirect(reverse("home1"))

    def handle_no_permission(self):
        return HttpResponseForbidden()
    def test_func(self):
        """Prevents logged users to acces to Sign_in view"""
        user = self.request.user
        if user.is_authenticated:
            return False
        else:
            return True
