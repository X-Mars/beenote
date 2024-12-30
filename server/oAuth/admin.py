from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'email', 'role', 'is_active', 'last_active_at', 'date_joined')
    list_filter = ('is_active', 'role', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('笔记权限', {'fields': ('note', 'note_group')}),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('重要日期', {'fields': ('last_login', 'last_active_at', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role', 'groups'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)


class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = '用户数量'


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
