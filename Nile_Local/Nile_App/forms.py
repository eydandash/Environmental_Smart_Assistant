# In this file I define the two different types of forms used across the web application, login form for signing in
# and registration form for signing up.
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserDetails


# Login Form
class LoginForm(ModelForm):
    # This is important since by default the generate input tag has type text, so won't treat it as password
    password = forms.CharField(widget=forms.PasswordInput())

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
        # Ensuring email1 and email2 have the same values
        e1 = cleaned_data.get("email")
        e2 = cleaned_data.get("email2")
        if e1 != e2:
            raise forms.ValidationError("Email addresses don't match")

# Registration Form - Extended
class UserDataForm(ModelForm):
    class Meta():
        model = UserDetails
        fields = ['company_name', 'company_address', 'contact_no']

    def clean(self):
        # Ensuring that any validation logic in parent classes is maintained
        cleaned_data = super().clean()
        # Ensuring the user enters  UK number using Regex as mentioned here
        # https://stackoverflow.com/questions/16405187/regular-expression-for-uk-mobile-number-python
        contact_no = cleaned_data.get("contact_no")
        rule = re.compile(r'^\+?(44)?(0|7)\d{9,13}$')
        if not rule.search(contact_no):
            raise forms.ValidationError("Please enter a valid UK number")


