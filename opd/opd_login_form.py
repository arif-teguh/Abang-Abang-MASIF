from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class OpdAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

    error_messages = {
        'invalid_login':
            "Email atau password salah, silahkan coba lagi"
        ,
        'inactive': "This account is inactive."
    }
    # widget = forms.TextInput(attrs={'class': 'myfieldclass'})
    # username = UsernameField(
    #     widget= forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'type': 'email'}))

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'email',
                'placeholder' : 'Email',
            }))

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class' : 'form-control',
            'type' : 'password',
            'placeholder' : 'Password',
        }),
    )
