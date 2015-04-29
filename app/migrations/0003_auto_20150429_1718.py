# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150429_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='name',
            new_name='title',
        ),
    ]
