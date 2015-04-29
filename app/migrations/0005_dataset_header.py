# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150429_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='header',
            field=models.TextField(null=True, blank=True),
        ),
    ]
