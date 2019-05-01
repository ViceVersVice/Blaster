
from django.urls import reverse, reverse_lazy
from allauth.account.views import LoginView
from allauth.socialaccount.models import SocialAccount
from django.views.generic.edit import UpdateView, DeleteView
from .forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin

class CustomLoginView(LoginView):
    template_name = "custom_allauth/allauth_login.html"
    def get_success_url(self):
        return reverse_lazy("homeT")

class DeleteSocialAccount(UserPassesTestMixin, DeleteView):
    model = SocialAccount
    pk_url_kwarg = "provider"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_user(self):
        return User.objects.get(id=self.kwargs.get("user_id", None))

    def get_object(self, queryset=None):
        sociall_accounts = SocialAccount.objects.filter(user=self.get_user())
        provider = self.kwargs.get("provider", None)
        sociall_account = sociall_accounts.get(provider=provider)
        return sociall_account

    def get_success_url(self):
        return reverse_lazy("current_user_profile", kwargs={"user_id": self.get_user().id})

    def test_func(self):
        requesting_user = self.request.user
        if requesting_user == self.get_user():
            return True
        else:
            return False
    def handle_no_permission(self):
        return HttpResponseForbidden()


class SetPasswordView(UpdateView):
    model = User
    template_name = "custom_allauth/set_password.html"
    pk_url_kwarg = "user_id"
    form_class = SetPasswordForm

    def form_valid(self, form):
        """After new password has been saved, Django logouts User from session,
        so we need to login User one more time"""
        user_obj = self.get_object() # User object
        self.object = form.save()
        backend = settings.AUTHENTICATION_BACKENDS[0] # ModelBackend
        auth_user = authenticate(username=user_obj.username, password=form.cleaned_data["password1"])
        login(self.request, auth_user, backend=backend)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("current_user_profile", kwargs={"user_id": self.request.user.id,})
