# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0025_productoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='option',
            field=models.CharField(default=django.utils.timezone.now, max_length=600),
            preserve_default=False,
        ),
    ]
