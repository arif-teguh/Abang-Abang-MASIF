from django import forms


class EditOpdProfileForm(forms.Form):
    phone_field = forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'pattern': '^\+?1?\d{3,15}$',
            'placeholder': 'Nomor telepon',
        }
    )

    phone = forms.CharField(
        max_length=15,
        min_length=1,
        widget=phone_field,
        label="Nomor Telepon "
    )

    alamat_field = forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Alamat',
        }
    )

    address = forms.CharField(
        max_length=120,
        min_length=1,
        widget=alamat_field,
        label="Alamat ",
    )
