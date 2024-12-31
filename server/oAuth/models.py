import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from note.models import Note, NoteGroup
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField('角色', max_length=20, default='user')
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
        db_table = 'user'
