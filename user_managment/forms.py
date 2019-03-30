from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import user_profile
from A.forms import sizeImageField
import datetime


class DatePick(forms.DateInput): #changing standart input type in html
    input_type = "date"
# class password_reset(forms.Form):
#     email = forms.EmailField(required=True)
class PasswordResetForm2(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except:
            raise forms.ValidationError(("User with this email doesn`t exist"), code="invalid")
        return email


class edit_user_profile_form(forms.ModelForm):
    class Meta:
        model = user_profile
        exclude = ["profile_related_user", "user_friends",]
        field_classes = { "user_image": sizeImageField, }
        labels = {
        "user_sex": "Sex", "user_description": "Some description...", "user_image": "Change Image",
        }
        widgets = {
        "birth_date": DatePick, "user_image": forms.FileInput,
        }
    def clean_birth_date(self):
        birth = self.cleaned_data["birth_date"]
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        birth_delta = datetime.date.today() - birth
        print(birth_delta)
        days = datetime.timedelta(days=3650)
        if birth_delta < days:
            raise forms.ValidationError(("Oh really??"), code="invalid") #birth date validayion
        return birth

class RegisterForm(UserCreationForm): #user registration form
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            exist = User.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(("This email is already used"), code="invalid")
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
