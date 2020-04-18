from django.db import models
from django.contrib.postgres.fields import ArrayField
from account.models import Account, UserProfile

class Lowongan(models.Model):
    choice = []
    judul = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    kuota_peserta = models.IntegerField()
    waktu_awal_magang = models.DateField()
    waktu_akhir_magang = models.DateField()
    batas_akhir_pendaftaran = models.DateField()
    berkas_persyaratan = ArrayField(
        models.CharField(max_length=100))
    deskripsi = models.TextField(max_length=1000)
    requirement = models.TextField(max_length=1000)
    is_lowongan_masih_berlaku = models.BooleanField(default=True)
    opd_foreign_key = models.ForeignKey(Account, on_delete=models.CASCADE,
                                        related_name='lowongan')
    list_pendaftar_key = models.ManyToManyField(UserProfile, null=True, blank=True)

    def __str__(self):
        return self.judul

class UserLamarMagang(models.Model):
    application_letter = models.TextField(max_length=2000)
    file_berkas_tambahan = models.FileField()
    lowongan_foreign_key = models.ForeignKey(Lowongan, on_delete=models.CASCADE,
                                             related_name='RelasiLowonganAndUser')
    user_foreign_key = models.ForeignKey(Account, on_delete=models.CASCADE,
                                         related_name='RelasiLowonganAndUser')
    status_lamaran = models.CharField(max_length=20, default="Pending")
    notes_status_lamaran = models.TextField(max_length=1000, default="Tidak Ada Catatan")
