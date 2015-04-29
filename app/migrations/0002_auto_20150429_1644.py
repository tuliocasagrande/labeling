# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='number_of_classes',
        ),
        migrations.AddField(
            model_name='dataset',
            name='class_column_name',
            field=models.CharField(default='class', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='has_header',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='number_of_classes',
            field=models.IntegerField(default=2),
        ),
    ]
