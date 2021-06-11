from django import forms
from .models import GENDER_CHOICE


class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    surname = forms.CharField(label='Your surname', max_length=100)
    gender = forms.ChoiceField(choices=GENDER_CHOICE, label='Gender')


class LoginForm(forms.Form):
    username = forms.CharField(label='Your name')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
