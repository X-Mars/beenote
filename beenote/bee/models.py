from django.db import models
from oauth.models import NewUser

# Create your models here.

class Note(models.Model):
    title = models.CharField('标题', max_length=9999)
    text = models.TextField('文章内容')
    type = models.CharField('文章类型', max_length=10, default='markdown')
    create_time = models.DateTimeField('创建时间')
    update_time = models.DateTimeField('更新时间')
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    notebook = models.ForeignKey('NoteBook', on_delete=models.CASCADE, blank=True, null=True, related_name='note')

    class Meta:
        verbose_name_plural = '笔记'

    def __str__(self):
        return self.title + '-' + self.user.name + '-' + self.type  + '-' + self.notebook.name

class NoteBook(models.Model):
    name = models.CharField('笔记本名称', max_length=10)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateTimeField('创建时间')

    class Meta:
        verbose_name_plural = '笔记本'

    def __str__(self):
        return self.name + '-' + self.user.name