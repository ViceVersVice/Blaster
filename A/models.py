from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User
class add_post(models.Model):
##    DA1 = "DAaa"
##    NIE1 = "nooo"
##    CHOICES = ((DA1, "yes"), (NIE1, "no"))
    post_related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_text = models.TextField(max_length=500)
    post_edition_date = models.DateTimeField(auto_now=True)
    post_publication_date = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to="post_images", blank=True)
    def __str__(self):
        return self.post_text

# Create your models here.
