from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from oauth.models import NewUser, Roles
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
class NewUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'roles')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('id', 'username', 'email', 'name', 'is_staff', 'is_active', 'last_login')
    list_display_links = ('id', 'username', 'email', 'name', 'last_login')

class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'roles')
    list_display_links = ('id', 'roles')

admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Roles, RolesAdmin)
