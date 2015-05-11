# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150509_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='number_of_samples',
            field=models.IntegerField(default=0),
        ),
    ]
