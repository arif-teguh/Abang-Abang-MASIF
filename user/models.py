from django.db import models


class UserVerificationList(models.Model):
    secret = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=50)
    creation_date = models.DateTimeField(
        verbose_name='creation date', auto_now_add=True)
