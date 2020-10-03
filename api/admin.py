from django.contrib import admin

# Register your models here.
from api.models import Department, AdditionalUserInfo

admin.site.register(Department)
admin.site.register(AdditionalUserInfo)
