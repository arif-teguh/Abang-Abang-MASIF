from django.contrib import admin

from account.models import Account, OpdProfile, AdminProfile, UserProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(OpdProfile)
admin.site.register(AdminProfile)
admin.site.register(UserProfile)
