# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_Gakki', '0005_auto_20171025_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
    ]
