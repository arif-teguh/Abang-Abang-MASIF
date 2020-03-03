from django import forms


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
