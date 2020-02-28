from django.contrib import admin

from account.models import Account, OpdProfile, AdminProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(OpdProfile)
admin.site.register(AdminProfile)
