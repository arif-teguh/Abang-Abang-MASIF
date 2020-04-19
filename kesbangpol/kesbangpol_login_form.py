from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

from account.models import Account

class KesbangpolAuthenticationForm(forms.Form):
    username = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'email',
                'placeholder' : 'Email',
            }))

    password = forms.CharField(
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class' : 'form-control',
            'type' : 'password',
            'placeholder' : 'Password',
        }),
    )

    def check(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        password = cleaned_data.get("password")
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise forms.ValidationError('User not exist')
        if not check_password(password, user.password):
            raise forms.ValidationError('Wrong Password')
        if user.is_kesbangpol is not True:
            raise forms.ValidationError('User restricted to this page')
        return cleaned_data
