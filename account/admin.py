from django.contrib import admin

from account.models import Account, OpdProfile, AdminProfile, PelamarProfile, KesbangpolProfile, UserProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(OpdProfile)
admin.site.register(AdminProfile)
admin.site.register(PelamarProfile)
admin.site.register(KesbangpolProfile)
admin.site.register(UserProfile)
