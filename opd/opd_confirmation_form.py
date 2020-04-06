from django import forms


class OpdConfirmationForm(forms.Form):
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
