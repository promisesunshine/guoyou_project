# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-12 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170512_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='\u6559\u5e08\u5934\u50cf'),
        ),
    ]
