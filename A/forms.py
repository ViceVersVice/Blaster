from django import forms
from .models import add_post
#from comment.models import comment


#class ValidatedImageField(forms.field):


class sizeImageField(forms.ImageField):
    """ImageField with customized Validation"""
    MAX_UPLOAD_SIZE = 2097152 # maximum image size in bytes
    def clean(self, data, initial=None):
        """Validates image size"""
        if data is not None:
            if data.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(("It`s too BIG, max. size 2 Mb"), code="invalid")
        return super().clean(data, initial=None)

class post_form(forms.ModelForm):
    """Post (question) ModelForm"""
    class Meta:
        model = add_post
        fields = ["post_title", "post_text",  "post_image", ]
        field_classes = { "post_image": sizeImageField, } # replaced form field class
        labels = {
            "post_title": "Title",
            "post_text": "Your question",
            "post_image": "Pictures",
        } # custom labels
    
