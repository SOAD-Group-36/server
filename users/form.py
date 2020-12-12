from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile')


class BusinessLoginForm(forms.Form):
    email = forms.CharField(max_length=80, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
