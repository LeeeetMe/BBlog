# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_Gakki', '0003_auto_20171025_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Blog_Gakki.userInfo', verbose_name='评论人'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
    ]
