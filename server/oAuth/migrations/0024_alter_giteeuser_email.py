# Generated by Django 5.1.7 on 2025-03-21 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oAuth', '0023_giteeconfig_giteeuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giteeuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱'),
        ),
    ]
