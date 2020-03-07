from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError("Users must have email address")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password)
        user.name = "SuperUser"
        user.phone = "000"
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    profile_picture = models.FileField(
        default="static/default-profile.png",
        max_length=500)
    name = models.CharField(max_length=128)
    email = models.EmailField(
        verbose_name="email", max_length=254, unique=True)
    phone = models.CharField(max_length=26)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_opd = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


class OpdProfile(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True, null=False, blank="False"
    )
    # Temporary Attribute
    unique_opd_attribute = models.CharField(max_length=60)

    def __str__(self):
        return "<OPD Profile> {}".format(self.unique_opd_attribute)


class AdminProfile(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True, null=False, blank="False"
    )
    # Temporary Attribute
    unique_admin_attribute = models.CharField(max_length=60)

    def __str__(self):
        return "<ADMIN Profile> {}".format(self.unique_admin_attribute)


class UserProfile(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
        null=False,
        blank=False,
    )

    born_date = models.DateField(default=datetime(1945, 8, 17))
    born_city = models.CharField(default='Not set', max_length=120)
    address = models.CharField(default='Not set', max_length=120)

    '''
    sex types
    m = male
    f = female
    n = not set
    '''

    sex = models.CharField(default='n', max_length=1)
    education = models.CharField(default='Not set', max_length=120)
    institution = models.CharField(default='Not set', max_length=120)
    major = models.CharField(default='Not set', max_length=120)

    def __str__(self):
        return "<USER Profile> Account : {}".format(self.user.email)
