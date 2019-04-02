from django.db import models
from A.models import add_post
from django.contrib.auth.models import User

class comment(models.Model):
    """Database Model for user post related comments.

    Attributes:
        comment_related_user: ForeignKey model field, defines relation of comments to
        it`s user (one to many relation).
        related_post: ForeignKey model field, defines relation of comments to it`s post (one to many relation).
        comment_text: TextField model field, defines comment text query_input
        comment_date: DateTimeField model field, defines date and time when comment was created
        comment_edition_date: DateTimeField model field, defines date and time when comment was last edited
    """

    comment_related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_post = models.ForeignKey(add_post, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_edition_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns: Human readable name of object"""
        return self.comment_text
    class Meta:
        """Comments ordering by most recent"""
        ordering = ["-comment_date"]
