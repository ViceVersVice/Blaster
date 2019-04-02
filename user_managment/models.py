from django.db import models
from django.contrib.auth.models import User

class user_profile(models.Model):
    """User profile model"""
    male = "Male"
    female = "Female"
    ND = "ND"
    last_activity = models.DateTimeField(auto_now=True) # last user activity
    sex_choices = [(ND, "ND"), (male, "Male"), (female, "Female"), ]
    profile_related_user = models.OneToOneField(User, on_delete=models.CASCADE) # related User object
    user_image = models.ImageField(upload_to="profile_images", blank=True) # profile image
    user_sex = models.CharField(max_length=6, choices=sex_choices, default=ND)
    birth_date = models.DateField(null=True)
    user_description = models.TextField(max_length="500",blank=True)
    #user_friends = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_friends")
    user_register_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.profile_related_user.username
# Create your models here.
