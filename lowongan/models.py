from django.db import models 
from account.models import Account
from django.contrib.postgres.fields import ArrayField
from django import forms


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class Lowongan(models.Model):
    choice = (
            ('Kartu Keluarga', 'Kartu Keluarga'),
            ('Kartu Tanda Penduduk', 'Kartu Tanda Penduduk'),
            ('Surat Izin Sekolah', 'Surat Izin Sekolah'),
        )
    judul = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    kuota_peserta = models.IntegerField()
    waktu_awal_magang = models.DateField()
    waktu_akhir_magang = models.DateField()
    batas_akhir_pendaftaran = models.DateField()
    berkas_persyaratan = ChoiceArrayField(
        base_field=models.CharField(max_length=256, choices=choice),
        default=list)
    deskripsi = models.TextField(max_length=1000)
    requirement = models.TextField(max_length=1000)
    is_lowongan_masih_berlaku = models.BooleanField(default=True)

    opd_foreign_key = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='lowongan')

    def __str__(self):
        return self.judul

   

#   Field penyedia diganti dengan kategori  ----- sudah

#   Naming Jangka waktu lamaran diganti dengan Batas Akhir Pendaftaran  ----- sudah

#   Field Jangka waktu lamaran diganti dengan kalender  ----- sudah

#   Field Durasi magang diganti dengan kalender (awal dan akhir)  ----- sudah

#   Naming berkas menjadi berkas persyaratan  ----- sudah

#   Field berkas diganti menjadi checkbox ------belum

#   Naming tenaga yang dibutuhkan diganti dengan kuota  ----- sudah