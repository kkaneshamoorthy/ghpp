# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 22:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0018_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]