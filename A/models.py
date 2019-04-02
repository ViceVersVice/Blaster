from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User
class add_post(models.Model):
    """Model for post"""
    post_related_user = models.ForeignKey(User, on_delete=models.CASCADE) # user
    post_title = models.CharField(max_length=200) # title
    post_text = models.TextField(max_length=500) # text
    post_edition_date = models.DateTimeField(auto_now=True) # post edition date
    post_publication_date = models.DateTimeField(auto_now_add=True) # post publication date
    post_image = models.ImageField(upload_to="post_images", blank=True) # post image (will be changed)
    def __str__(self):
        return self.post_text
    class Meta:
        """Comments ordering by most recent"""
        ordering = ["-post_edition_date"]
# Create your models here.
