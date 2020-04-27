from django import forms

from account.models import Account
from admin.models import OpdVerificationList

class OpdRegistrationForm(forms.Form):
    opd_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Nama OPD',
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

    def check(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        err = []
        try:
            Account.objects.get(email=email)
            raise forms.ValidationError('OPD Already registered')
        except Account.DoesNotExist as e:
            err = e
        try:
            OpdVerificationList.objects.get(email=email)
            raise forms.ValidationError(
                'Please check your inbox for verification')
        except OpdVerificationList.DoesNotExist as e:
            err = e
        return err
