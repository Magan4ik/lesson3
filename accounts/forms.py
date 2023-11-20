from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from accounts.models import Profile

import datetime

User = get_user_model()

YEARS = list(range(1901, datetime.datetime.now().year + 1))

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput()
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class ProfileForm(ModelForm):
    avatar = forms.URLField(
        label="Avatar url",
        widget=forms.URLInput(),
        required=False
    )
    gender = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=Profile.GENDER_CHOICES
    )
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS)
    )
    info = forms.CharField()

    class Meta:
        model = Profile
        fields = ["avatar", "gender", "date_of_birth", "info"]
