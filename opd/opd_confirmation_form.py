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
    
    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('clean_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
