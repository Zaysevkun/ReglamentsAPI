from django.contrib import admin
from api.models import User
from django.contrib.auth.models import User as BasicUser
from django.contrib.auth.admin import UserAdmin as BasicUserAdmin


# Register your models here.

class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(BasicUserAdmin):
    inlines = (UserInline,)


admin.site.unregister(BasicUser)
admin.site.register(User)

