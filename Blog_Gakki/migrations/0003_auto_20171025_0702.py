# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog_Gakki', '0002_auto_20171025_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.IntegerField(default=0, verbose_name='所属楼层'),
        ),
    ]
