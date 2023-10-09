from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    # add any other custom fields or configurations

admin.site.register(CustomUser)
admin.site.register(CustomRoles)
admin.site.register(CustomPermissions)
admin.site.register(RolePermissionAssociation)
admin.site.register(Projects)
admin.site.register(VDML_Document)
