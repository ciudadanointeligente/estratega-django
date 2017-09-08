# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estrategias', '0006_auto_20170901_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actorrelevante',
            name='objetivo',
        ),
        migrations.RemoveField(
            model_name='barrera',
            name='objetivo',
        ),
        migrations.RemoveField(
            model_name='factorhabilitante',
            name='objetivo',
        ),
        migrations.RemoveField(
            model_name='resultadointermedio',
            name='objetivo',
        ),
        migrations.RenameField(
            model_name='objetivo',
            old_name='texto',
            new_name='objetivo',
        ),
        migrations.AddField(
            model_name='objetivo',
            name='barreras',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='objetivo',
            name='factoreshabilitantes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objetivo',
            name='resultadosintermedios',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ActorRelevante',
        ),
        migrations.DeleteModel(
            name='Barrera',
        ),
        migrations.DeleteModel(
            name='FactorHabilitante',
        ),
        migrations.DeleteModel(
            name='ResultadoIntermedio',
        ),
    ]
