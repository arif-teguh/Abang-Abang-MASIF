from django.db import models 
from account.models import Account

class Lowongan(models.Model):
    judul = models.CharField(max_length=100)
    penyedia = models.CharField(max_length=100)
    jumlah_tersedia = models.IntegerField()
    durasi_magang = models.IntegerField()
    jangka_waktu_lamaran = models.IntegerField()
    berkas = models.CharField(max_length=100)
    deskripsi = models.TextField(max_length=1000)
    requirement = models.TextField(max_length=1000)

    opd_foreign_key = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.judul