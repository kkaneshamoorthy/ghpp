# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_auto_20170723_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extras',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]
