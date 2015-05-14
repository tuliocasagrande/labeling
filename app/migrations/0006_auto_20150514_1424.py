# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150512_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='label_name',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='header',
            field=models.TextField(default='header'),
            preserve_default=False,
        ),
    ]
