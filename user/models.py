from django.db import models


class UserVerificationList(models.Model):
    secret = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=80)
    creation_date = models.DateTimeField(
        verbose_name='creation date', auto_now_add=True)
