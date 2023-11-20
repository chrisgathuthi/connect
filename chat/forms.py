from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={"class": "password", "placeholder": "create password"}), label="Password")
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={"class": "password", "placeholder": "confirm password"}), label="Confirm password")

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "password1": "Password",
            "password2": "Confirm password"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
        }