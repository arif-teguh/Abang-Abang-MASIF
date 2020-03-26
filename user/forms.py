from django import forms

from account.models import UserProfile, Account


class EditUserProfileForm(forms.Form):
    string_field = forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Nama',
        }
    )

    date_field = forms.TextInput(
        attrs={
            'class': 'datepicker',
            'autocomplete': 'off'

        }
    )

    text_area_field = forms.Textarea(
        attrs={
            'class': 'form-control',
            'type': 'text',
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

    born_date = forms.CharField(widget=date_field)

    string_field.attrs['placeholder'] = 'Alamat'
    address = forms.CharField(
        max_length=300,
        min_length=1,
        widget=text_area_field,
    )
    sex = forms.ChoiceField(choices=[('m', 'Laki - Laki'), ('f', 'Perempuan')], widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    string_field.attrs['placeholder'] = 'Pendidikan'
    education = forms.ChoiceField(choices=[
        ('s1', 'S1'),
        ('d4', 'D4'),
        ('d3', 'D3'),
        ('d1', 'D2'),
        ('d1', 'D1'),
        ('smk', 'SMK'),
        ('sma', 'SMA'),
    ],
        widget=forms.Select(attrs={
            'class': 'form-control',
        }))

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

    phone_field = forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'pattern': '^\+?1?\d{3,15}$',
            'placeholder': 'Nomor telepon',
        }
    )
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = forms.CharField(
        max_length=100,
        min_length=1,
        widget=phone_field,
    )


class CVForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cv',)


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('profile_picture',)
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'black'}),
        }
