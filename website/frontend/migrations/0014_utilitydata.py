# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-01 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0013_auto_20170726_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtilityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('info', models.CharField(max_length=200)),
            ],
        ),
    ]