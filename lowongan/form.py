from django import forms
from .models import Lowongan

class LowonganForm(forms.ModelForm):

    class Meta:

        attribute_text_input = {
        'class' : 'form-control col-6'
        }
        attribute_date_input = {
        'class' : 'form-control col-2', 'type':'date'
        }
        attribute_sel_input = {
        'class':'form-control col-6 selectpicker'
        }
        attribute_text_area = {
            'class' : 'form-control col-8',
            'rows'  : "5"
        }
        model = Lowongan
        fields = [
            "judul", "kategori", "kuota_peserta",
            "waktu_awal_magang", "waktu_akhir_magang",
            "batas_akhir_pendaftaran", "berkas_persyaratan",
            "deskripsi", "requirement"
        ]
        widgets = {
            "judul" : forms.TextInput(attrs=attribute_text_input),
            "kategori" : forms.TextInput(attrs=attribute_text_input),
            "kuota_peserta" : forms.TextInput(attrs=attribute_text_input),
            "waktu_awal_magang" : forms.DateInput(attrs=attribute_date_input),
            "waktu_akhir_magang" : forms.DateInput(attrs=attribute_date_input),
            "batas_akhir_pendaftaran" : forms.DateInput(attrs=attribute_date_input),
            "berkas_persyaratan" : forms.SelectMultiple(attrs=attribute_sel_input),
            "deskripsi" : forms.Textarea(attrs=attribute_text_area),
            "requirement" : forms.Textarea(attrs=attribute_text_area),

        }
        labels = {
            "judul" : "Judul Magang",
            "kategori" : "Kategori Magang",
            "kuota_peserta" : "Kuota Magang",
            "waktu_awal_magang" : "Tanggal Magang Dimulai",
            "waktu_akhir_magang" : "Tanggal Magang Selesai",
            "batas_akhir_pendaftaran" : "Batas Akhir Pendaftaran Magang",
            "berkas_persyaratan" : "Berkas Persyaratan Magang",
            "deskripsi" : "Deskripsi Magang",
            "requirement" : "Requirement Magang",
        } 


