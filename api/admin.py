from django.contrib import admin

# Register your models here.
from api.models import Department, User

admin.site.register(Department)
admin.site.register(User)