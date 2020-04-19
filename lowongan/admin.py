from django.contrib import admin

# Register your models here.
from lowongan.models import Lowongan, UserLamarMagang

admin.site.register(Lowongan)
admin.site.register(UserLamarMagang)