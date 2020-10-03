from django.contrib import admin

# Register your models here.
from api.models import Department, AdditionalUserInfo, Regulations, Revisions

admin.site.register(Department)
admin.site.register(AdditionalUserInfo)
admin.site.register(Regulations)
admin.site.register(Revisions)
