from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )