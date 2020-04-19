from django import forms

from account.models import Account
from .models import UserVerificationList

class UserRegistrationForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Nama Pelamar',
            }))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'user@email.com',
            }))
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Nomor Telepon',
            }))
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Ketikkan Password Anda',
            }))
    confirm_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Ketik Ulang Password Anda',
            }))

    def check(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        err = []
        try:
            Account.objects.get(email=email)
            raise forms.ValidationError("Email is already registered!",
                                        code='email_exist')
        except Account.DoesNotExist as e:
            err = e
        try:
            UserVerificationList.objects.get(email=email)
            raise forms.ValidationError(
                "Check your inbox for confirmation link",
                code='confirm_email')
        except UserVerificationList.DoesNotExist as e:
            err = e
        return err
