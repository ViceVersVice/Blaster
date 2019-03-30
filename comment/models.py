from django.db import models
from A.models import add_post
from django.contrib.auth.models import User
class comment(models.Model):
    comment_related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(add_post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_edition_date = models.DateTimeField(auto_now=True)
    #comment_image = models.ImageField(upload_to="comment_images", blank=True)
    def __str__(self):
        return self.comment_text
    class Meta:
        ordering = ["-comment_date"]

# Create your models here.
