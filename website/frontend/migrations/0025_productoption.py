# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-01 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0024_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optionCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.OptionCategory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.Product')),
            ],
        ),
    ]
