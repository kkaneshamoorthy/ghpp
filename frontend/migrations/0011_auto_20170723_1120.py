# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-23 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_auto_20170723_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productextras',
            name='extra_id',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='productextras',
            name='product_id',
            field=models.IntegerField(max_length=50),
        ),
    ]
