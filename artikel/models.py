from django.db import models

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    waktu_dibuat = models.DateTimeField(auto_now=True)
    foto_artikel = models.FileField(null=True, blank=True)
