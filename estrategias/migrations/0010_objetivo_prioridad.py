# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estrategias', '0009_auto_20170908_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='objetivo',
            name='prioridad',
            field=models.IntegerField(default=100),
        ),
    ]
