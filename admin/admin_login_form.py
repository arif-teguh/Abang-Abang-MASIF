from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class AdminAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

    error_messages = {
        'invalid_login':
            "Email atau password salah, silahkan coba lagi"
        ,
        'inactive': "This account is inactive."
    }

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email',
            }
        )
    )

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password',
        }),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        elif not user.is_admin:
            raise forms.ValidationError(
                'Anda bukan Admin MASIF, '
                'Silahkan login menggunakan akun admin MASIF',
                code='notadmin'
            )
