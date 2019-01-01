from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class NewUser(AbstractUser):
    name = models.CharField(_('name'), max_length=150)
    roles = models.ManyToManyField('Roles', blank=True)
    jwt_secret = models.UUIDField(default=uuid.uuid4())

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        pass

    def __str__(self):
        return self.username + '-' + self.name

class Roles(models.Model):
    roles = models.CharField('角色', max_length=10, default='users')

    class Meta:
        verbose_name_plural = '用户角色'

    def __str__(self):
        return self.roles

def jwt_get_secret_key(NewUser):
    return NewUser.jwt_secret
