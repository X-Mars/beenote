from django.db import models
from django.conf import settings

class NoteGroup(models.Model):
    name = models.CharField('名称', max_length=100)
    description = models.TextField('描述', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name='创建者'
    )

    class Meta:
        db_table = 'note_group'
        verbose_name = '笔记分组'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    group = models.ForeignKey(
        NoteGroup,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='所属分组'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='创建者'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'note'
        verbose_name = '笔记'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
