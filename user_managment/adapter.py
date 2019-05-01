from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from .models import user_profile
from django.utils import timezone
from django.contrib.auth.models import User

class CustomAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """If it is new signup with socialaccount, redirect to set password"""
        try:
            has_user_profile = request.user.user_profile
            has_user_profile.last_activity = timezone.now()
            has_user_profile.save()
            path = reverse("homeT")

        except:
            # For new users redirect to profile page to configure passwords and etc.
            path = reverse("set_password", kwargs={"user_id": request.user.id})
        return path


class CustomSocialAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """If user is already registered and do not have socialaccount,
        after login sociallaccount will be automatically connected (bypassing new user sign up).
        More: https://stackoverflow.com/questions/19354009/django-allauth-social-login-automatically-linking-social-site-profiles-using-th/30591838#30591838"""
        if sociallogin.is_existing:
            return
        email = sociallogin.account.extra_data['email'].lower()
        try:
            user_obj = User.objects.get(email=email)
        except:
            return
        sociallogin.connect(request, user_obj)

    def get_connect_redirect_url(self, request, socialaccount):
        return reverse("current_user_profile", kwargs={"user_id": request.user.id})
