from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=20, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active_at = models.DateTimeField('最近活跃时间', null=True, blank=True)

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

    class Meta:
        db_table = 'user'
