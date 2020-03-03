from django.db import models

class OpdVerificationList(models.Model):
    secret = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    creation_date = models.DateTimeField(
        verbose_name='creation date', auto_now_add=True)
