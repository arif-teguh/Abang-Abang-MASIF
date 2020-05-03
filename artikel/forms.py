from django import forms
from .models import Artikel

class ArtikelForm(forms.ModelForm):
    class Meta:
        attribute_text_input = {
            'class' : 'form-control col-6'
        }
        attribute_text_area = {
            'class' : 'form-control col-8',
            'rows'  : "5"
        }
        model = Artikel
        fields = [
            "judul", "foto_artikel", "deskripsi"
        ]
        widgets = {
            "judul" : forms.TextInput(
                attrs=attribute_text_input
            ),
            "deskripsi" : forms.Textarea(
                attrs=attribute_text_area
            )
        }
        labels = {
            "foto_artikel" : "Foto Sampul Artikel"
        }
