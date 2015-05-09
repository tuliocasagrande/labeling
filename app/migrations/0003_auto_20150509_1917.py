# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150507_1423'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([('dataset', 'contributor')]),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set([('sample', 'owner')]),
        ),
    ]
