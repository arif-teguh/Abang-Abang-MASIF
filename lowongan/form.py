from django import forms
from .models import Lowongan

class LowonganForm(forms.ModelForm):
    
    class Meta:
        attribute_text_input = {
        'class' : 'form-control col-6'
        }
        attribute_text_area = {
            'class' : 'form-control col-8',
            'rows'  : "5"
        }
        model = Lowongan
        fields = [
            "judul", "penyedia", "jumlah_tersedia", 
            "durasi_magang", "jangka_waktu_lamaran", 
            "berkas", "deskripsi", "requirement"
        ]
        widgets = {
            "judul" : forms.TextInput(attrs=attribute_text_input),
            "penyedia" : forms.TextInput(attrs=attribute_text_input),
            "jumlah_tersedia" : forms.TextInput(attrs=attribute_text_input),
            "durasi_magang" : forms.TextInput(attrs=attribute_text_input),
            "jangka_waktu_lamaran" : forms.TextInput(attrs=attribute_text_input),
            "berkas" : forms.TextInput(attrs=attribute_text_input),
            "deskripsi" : forms.Textarea(attrs=attribute_text_area),
            "requirement" : forms.Textarea(attrs=attribute_text_area),

        }


