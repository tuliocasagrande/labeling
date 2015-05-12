# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150511_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='original_index',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sample',
            name='times_labeled',
            field=models.IntegerField(default=0),
        ),
    ]
