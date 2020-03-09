from django import forms


class EditUserProfileForm(forms.Form):
    string_field = forms.TextInput(
        attrs={
            'autofocus': True,
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Nama',
        }
    )

    name = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )
    string_field.attrs['placeholder'] = 'Kota lahir'
    born_city = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )
    born_date = forms.DateField()

    string_field.attrs['placeholder'] = 'Alamat'
    address = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )
    sex = forms.ChoiceField(choices=[('m', 'Laki - Laki'), ('f', 'Perempuan')])

    string_field.attrs['placeholder'] = 'Pendidikan'
    education = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )

    string_field.attrs['placeholder'] = 'Institusi'
    institution = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )

    string_field.attrs['placeholder'] = 'Jurusan'
    major = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )

    string_field.attrs['placeholder'] = 'Nomor telepon'
    phone = forms.CharField(
        max_length=100,
        min_length=1,
        widget=string_field,
    )
