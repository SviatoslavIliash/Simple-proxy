from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser, MySite


class LoginForm(forms.Form):
    username = forms.CharField(label="Your login", max_length=100, widget=forms.TextInput(
                                      attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(
                                      attrs={"class": "form-control"}))


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Your login", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(
        attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Repeat Password", max_length=100, widget=forms.PasswordInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']


class UserForm(ModelForm):
    username = forms.CharField(label="Your login", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control", 'readonly': 'readonly'}))
    first_name = forms.CharField(label="First name", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last name", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    email = forms.CharField(label="Email", max_length=100, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    info = forms.CharField(label="Describe", max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    image = forms.ImageField(label="Photo")

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "info", "image"]


class MySiteForm(ModelForm):
    alias = forms.CharField(label="Site Alias:", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    alias_url = forms.URLField(label="Site URL:", max_length=100, widget=forms.URLInput(
        attrs={"class": "form-control"}))
    visit_counter = forms.IntegerField(required=False)
    data_in = forms.IntegerField(required=False)
    data_out = forms.IntegerField(required=False)

    class Meta:
        model = MySite
        fields = ["alias", "alias_url", "visit_counter", "data_in", "data_out"]
