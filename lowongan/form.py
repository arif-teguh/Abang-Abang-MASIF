from django import forms
from .models import Lowongan

class LowonganForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.id_lowongan = kwargs.pop("id", None)
        self.list_choice = kwargs.pop("list_choice", None)
        self.choice = ()
        super(LowonganForm, self).__init__(*args, **kwargs)
        if self.id_lowongan is not None:
            obj_lowongan_by_id = Lowongan.objects.get(pk=self.id_lowongan)
            self.choice = ((i, i)for i in obj_lowongan_by_id.berkas_persyaratan)
        elif self.list_choice is not None:
            self.choice = ((i, i)for i in self.list_choice)
        else:
            self.choice = (
                ('Kartu Keluarga', 'Kartu Keluarga'),
                ('Kartu Tanda Penduduk', 'Kartu Tanda Penduduk'),
                ('Surat Izin Sekolah', 'Surat Izin Sekolah'),
            )
        self.fields['berkas_persyaratan'].choices = self.choice
        self.fields['berkas_persyaratan'].widget.choices = self.choice

    def clean(self):
        cleaned_data = super(LowonganForm, self).clean()
        try:
            if cleaned_data["waktu_awal_magang"] > cleaned_data["waktu_akhir_magang"]:
                self.add_error('waktu_awal_magang',
                               "Tanggal awal lebih besar dari tanggal akhir")
                self.add_error('waktu_akhir_magang',
                               "Tanggal awal lebih besar dari tanggal akhir")
                return cleaned_data
        except KeyError:
            pass

    class Meta:
        attribute_text_input = {
            'class' : 'form-control col-6'
        }
        attribute_date_input = {
            'class' : 'form-control col-2', 'type':'date'
        }
        attribute_sel_input = {
            'class':'form-control col-5 selectpicker'
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
            "judul" : forms.TextInput(
                attrs=attribute_text_input),

            "kategori" : forms.TextInput(
                attrs=attribute_text_input),

            "kuota_peserta" : forms.TextInput(
                attrs=attribute_text_input),

            "waktu_awal_magang" : forms.DateInput(
                attrs=attribute_date_input),

            "waktu_akhir_magang" : forms.DateInput(
                attrs=attribute_date_input),

            "batas_akhir_pendaftaran" : forms.DateInput(
                attrs=attribute_date_input),

            "berkas_persyaratan" : forms.SelectMultiple(
                attrs=attribute_sel_input, choices=[]),

            "berkas_persyaratan_lainnya" : forms.HiddenInput(),

            "deskripsi" : forms.Textarea(
                attrs=attribute_text_area),

            "requirement" : forms.Textarea(
                attrs=attribute_text_area),

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
