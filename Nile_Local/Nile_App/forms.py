# In this file I define the two different types of forms used across the web application, login form for signing in
# and registration form for signing up.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserDetails


# Login Form
class LoginForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'password']


# Registration form
class UserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    email2 = forms.EmailField(widget=forms.EmailInput())

    class Meta():
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'email2']

    # Overrriding the built-in validation for django forms, since they originally don't check for 2 emails
    def clean(self):
        # Ensuring that any validation logic in parent classes is maintained
        cleaned_data = super().clean()
        e1 = cleaned_data.get("email")
        e2 = cleaned_data.get("email2")
        if e1 != e2:
            raise forms.ValidationError("Email addresses don't match")



# Registration Form - Extended
class UserDataForm(ModelForm):
    class Meta():
        model = UserDetails
        fields = ['company_name', 'company_address', 'contact_no']
