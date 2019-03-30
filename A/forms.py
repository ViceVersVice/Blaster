from django import forms
from .models import add_post
#from comment.models import comment


#class ValidatedImageField(forms.field):


class sizeImageField(forms.ImageField):
    MAX_UPLOAD_SIZE = 2097152
    def clean(self, data, initial=None):
        if data is not None:
            if data.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(("It`s too BIG, max. size 2 Mb"), code="invalid")
        return super().clean(data, initial=None)

class post_form(forms.ModelForm):
    class Meta:
        model = add_post
        fields = ["post_title", "post_text",  "post_image", ]
        field_classes = { "post_image": sizeImageField, }
        labels = {
            "post_title": "Title",
            "post_text": "Your question",
            "post_image": "Pictures",
        }
    # def clean_post_image(self, *args, **kwargs):
    #     data = self.cleaned_data['post_image']
    #     if data.size > MAX_UPLOAD_SIZE:
    #         raise forms.ValidationError("It`s too BIG")
    #
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     return data
