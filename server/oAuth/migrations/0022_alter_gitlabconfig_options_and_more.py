# Generated by Django 5.1.7 on 2025-03-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oAuth', '0021_gitlabconfig_gitlabuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitlabconfig',
            options={'ordering': ['-created_at'], 'verbose_name': 'GitLab 配置', 'verbose_name_plural': 'GitLab 配置'},
        ),
        migrations.AddField(
            model_name='gitlabconfig',
            name='gitlab_server',
            field=models.CharField(default='https://gitlab.com', max_length=255, verbose_name='GitLab 服务器地址'),
        ),
        migrations.AlterField(
            model_name='gitlabconfig',
            name='client_id',
            field=models.CharField(max_length=255, verbose_name='Client ID'),
        ),
        migrations.AlterField(
            model_name='gitlabconfig',
            name='client_secret',
            field=models.CharField(max_length=255, verbose_name='Client Secret'),
        ),
        migrations.AlterField(
            model_name='gitlabconfig',
            name='redirect_uri',
            field=models.CharField(blank=True, default='1', max_length=255, verbose_name='重定向URI'),
            preserve_default=False,
        ),
    ]
