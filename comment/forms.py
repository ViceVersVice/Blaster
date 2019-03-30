from django import forms
from A.forms import sizeImageField
from .models import comment


class comment_form(forms.ModelForm):
    class Meta:
        model = comment
        fields = ["comment_text", ]
        labels = {'comment_text': "Your answer",}
        #     "comment_image": "Some images",
        # }
        # field_classes = { "comment_image": sizeImageField, }

"""class post_form(forms.Form):
    comment = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label='comment',
    )"""
