import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from note.models import Note, NoteGroup
from django.utils import timezone


class User(AbstractUser):
    role_choices = [
        ('user', '普通用户'),
        ('admin', '管理员'),
        ('superuser', '超级管理员'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField('角色', choices=role_choices, default='user', max_length=20)
    avatar = models.URLField('头像', max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active_at = models.DateTimeField('最后活跃时间', default=timezone.now)

    # 添加 related_name 来解决冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='oauth_user_set',
        related_query_name='oauth_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='oauth_user_set',
        related_query_name='oauth_user'
    )

    note = models.ManyToManyField(
        Note,
        related_name='note_users',
        verbose_name='授权笔记',
        blank=True,
    )

    note_group = models.ManyToManyField(
        NoteGroup,
        related_name='note_group_users',
        verbose_name='授权分组',
        blank=True,
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username + ' - ' + self.role


class WeComConfig(models.Model):
    """企业微信配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    corp_id = models.CharField('企业ID', max_length=100)
    agent_id = models.CharField('应用ID', max_length=100)
    secret = models.CharField('应用密钥', max_length=100)
    redirect_uri = models.URLField('回调域名', max_length=500, null=True, blank=True)
    enabled = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '企业微信配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'企业微信配置 - {self.corp_id}'


class FeiShuConfig(models.Model):
    """飞书配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_id = models.CharField('应用ID', max_length=100)
    app_secret = models.CharField('应用密钥', max_length=100)
    redirect_uri = models.URLField('回调域名', max_length=500, null=True, blank=True)
    enabled = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '飞书配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'飞书配置 - {self.app_id}'

class DingTalkConfig(models.Model):
    """钉钉配置"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField('Client ID', max_length=100)
    client_secret = models.CharField('Client Secret', max_length=100)
    app_id = models.CharField('APP ID', max_length=100)
    redirect_uri = models.URLField('回调域名', max_length=500, null=True, blank=True)
    enabled = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '钉钉配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'钉钉配置 - {self.client_id}'


class WeComUser(models.Model):
    """企业微信用户"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wecom_info', null=True, blank=True)
    wecom_user_id = models.CharField('企业微信用户ID', max_length=100)
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    avatar = models.URLField('头像', max_length=500, null=True, blank=True)
    qr_code = models.URLField('二维码', max_length=500, null=True, blank=True)
    mobile = models.CharField('手机号', max_length=20, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, null=True, blank=True)
    address = models.CharField('地址', max_length=200, null=True, blank=True)
    position = models.CharField('职位', max_length=100, null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=[
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知')
    ], default='unknown')
    department = models.CharField('部门', max_length=100, null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=[
        ('active', '在职'),
        ('inactive', '离职'),
        ('pending', '待确认')
    ], default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '企业微信用户'
        verbose_name_plural = verbose_name
        unique_together = [('wecom_user_id',)]

    def __str__(self):
        return f'企业微信用户 - {self.name or self.user.username}'


class FeiShuUser(models.Model):
    """飞书用户"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feishu_info', null=True, blank=True)
    open_id = models.CharField('飞书用户ID', max_length=100)
    union_id = models.CharField('统一ID', max_length=100, null=True, blank=True)
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    avatar = models.URLField('头像', max_length=500, null=True, blank=True)
    mobile = models.CharField('手机号', max_length=20, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, null=True, blank=True)
    tenant_key = models.CharField('企业标识', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '飞书用户'
        verbose_name_plural = verbose_name
        unique_together = [('open_id',)]

    def __str__(self):
        return f'飞书用户 - {self.name or self.user.username}'


class DingTalkUser(models.Model):
    """钉钉用户"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dingtalk_info', null=True, blank=True)
    open_id = models.CharField('钉钉用户ID', max_length=100)
    union_id = models.CharField('统一ID', max_length=100, null=True, blank=True)
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    avatar = models.URLField('头像', max_length=500, null=True, blank=True)
    mobile = models.CharField('手机号', max_length=20, null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, null=True, blank=True)
    position = models.CharField('职位', max_length=100, null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=[
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知')
    ], default='unknown')
    department = models.CharField('部门', max_length=100, null=True, blank=True)
    job_number = models.CharField('工号', max_length=100, null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=[
        ('active', '在职'),
        ('inactive', '离职'),
        ('pending', '待确认')
    ], default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '钉钉用户'
        verbose_name_plural = verbose_name
        unique_together = [('open_id',)]

    def __str__(self):
        return f'钉钉用户 - {self.name or self.user.username}'
