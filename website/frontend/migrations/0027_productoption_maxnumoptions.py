# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-10 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0026_order_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoption',
            name='maxNumOptions',
            field=models.CharField(default=django.utils.timezone.now, max_length=6),
            preserve_default=False,
        ),
    ]
