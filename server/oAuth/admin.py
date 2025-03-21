from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import (
    User, WeComConfig, FeiShuConfig, 
    DingTalkConfig, WeComUser, FeiShuUser, DingTalkUser,
    GitHubConfig, GitHubUser, GoogleConfig, GoogleUser,
    GitLabConfig, GitLabUser
)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'email', 'is_active', 'last_active_at', 'date_joined')
    list_filter = ('is_active', 'role', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'role', 'avatar')}),
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


@admin.register(WeComConfig)
class WeComConfigAdmin(admin.ModelAdmin):
    list_display = ('corp_id', 'agent_id', 'secret', 'redirect_uri', 'enabled', 'created_at', 'updated_at')
    list_filter = ('enabled',)
    search_fields = ('corp_id', 'agent_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('corp_id', 'agent_id', 'secret', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(FeiShuConfig)
class FeiShuConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'app_secret', 'redirect_uri', 'enabled', 'created_at', 'updated_at')
    list_filter = ('enabled',)
    search_fields = ('app_id',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('app_id', 'app_secret', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DingTalkConfig)
class DingTalkConfigAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'client_id', 'client_secret', 'redirect_uri', 'enabled', 'created_at', 'updated_at')
    list_filter = ('enabled',)
    search_fields = ('app_id', 'client_id', 'client_secret')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('app_id', 'client_id', 'client_secret', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(WeComUser)
class WeComUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'mobile', 'email', 'position', 'department', 'status')
    list_filter = ('status', 'gender', 'department')
    search_fields = ('name', 'mobile', 'email', 'user__username')
    # raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'wecom_user_id', 'status')
        }),
        ('基本信息', {
            'fields': ('name', 'gender', 'mobile', 'email', 'position', 'department')
        }),
        ('其他信息', {
            'fields': ('avatar', 'qr_code', 'address')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(FeiShuUser)
class FeiShuUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'mobile', 'email')
    # list_filter = ('status', )
    search_fields = ('name', 'mobile', 'email', 'user__username')
    # raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'open_id', 'union_id')
        }),
        ('基本信息', {
            'fields': ('name', 'mobile', 'email')
        }),
        ('其他信息', {
            'fields': ('avatar',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DingTalkUser)
class DingTalkUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'mobile', 'email', 'position', 'department', 'status')
    list_filter = ('status', 'gender', 'department')
    search_fields = ('name', 'mobile', 'email', 'user__username', 'job_number')
    # raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'open_id', 'union_id', 'status')
        }),
        ('基本信息', {
            'fields': ('name', 'gender', 'mobile', 'email', 'position', 'department', 'job_number')
        }),
        ('其他信息', {
            'fields': ('avatar',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GitHubConfig)
class GitHubConfigAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'client_secret', 'redirect_uri', 'enabled', 'created_at', 'updated_at')
    list_filter = ('enabled',)
    search_fields = ('client_id',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('client_id', 'client_secret', 'redirect_uri', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GitHubUser)
class GitHubUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'login', 'email', 'github_id')
    search_fields = ('name', 'login', 'email', 'user__username', 'github_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'github_id', 'login')
        }),
        ('基本信息', {
            'fields': ('name', 'email', 'avatar_url', 'bio', 'location')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GoogleConfig)
class GoogleConfigAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'client_secret', 'redirect_uri', 'enabled', 'created_at', 'updated_at')
    list_filter = ('enabled',)
    search_fields = ('client_id',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('client_id', 'client_secret', 'redirect_uri', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GoogleUser)
class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'google_id')
    search_fields = ('name', 'email', 'user__username', 'google_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'google_id', 'email')
        }),
        ('基本信息', {
            'fields': ('name', 'given_name', 'family_name', 'picture', 'locale')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(GitLabConfig)
class GitLabConfigAdmin(admin.ModelAdmin):
    """GitLab 配置管理"""
    list_display = ('client_id', 'gitlab_server', 'redirect_uri', 'enabled', 'created_at')
    list_filter = ('enabled',)
    search_fields = ('client_id', 'gitlab_server')
    fieldsets = (
        ('基本信息', {
            'fields': ('client_id', 'client_secret', 'gitlab_server', 'redirect_uri', 'enabled')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GitLabUser)
class GitLabUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'username', 'email', 'gitlab_id')
    search_fields = ('name', 'username', 'email', 'user__username', 'gitlab_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'gitlab_id', 'username')
        }),
        ('基本信息', {
            'fields': ('name', 'email', 'avatar_url', 'web_url')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
