from django import forms
from A.forms import sizeImageField
from .models import comment


class comment_form(forms.ModelForm):
    """ModelForm for comment input"""
    class Meta:
        model = comment # model object
        fields = ["comment_text", ]
        labels = {'comment_text': "Your answer",} # form fields labels

        #     "comment_image": "Some images",
        # }
        # field_classes = { "comment_image": sizeImageField, }
