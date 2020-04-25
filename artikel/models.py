from django.db import models

class Artikel(models.Model):
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    waktu_dibuat = models.DateTimeField(auto_now=True)
