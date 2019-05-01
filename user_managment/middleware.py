from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from .models import user_profile


class LastActivity():
    """Middleware for autologout inactive users.
    Is engaged in session expiration and automatic logout of inactive users"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Logout of inactive users"""
        response = self.get_response(request)
        session_age = timedelta(seconds=86400) #24 hours
        if request.user.is_authenticated and request.user.is_staff == False:
            user_id = request.user.id
            try:
                last_activity = user_profile.objects.get(profile_related_user=user_id).last_activity
            except:
                new_user = User.objects.get(id=user_id)
                new_profile = user_profile.objects.create(profile_related_user=new_user, last_activity=timezone.now())
                last_activity = new_profile.last_activity
            if timezone.now() - last_activity > session_age:
                print("LOGGED_OUT", last_activity)
                logout(request)
            else:
                user_profile.objects.filter(profile_related_user=user_id).update(last_activity=timezone.now())
        return response
