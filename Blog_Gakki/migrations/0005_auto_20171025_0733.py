# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_Gakki', '0004_auto_20171025_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间'),
        ),
    ]