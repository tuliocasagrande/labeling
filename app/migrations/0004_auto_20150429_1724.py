# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150429_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='class_column_name',
            new_name='label_column_name',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='number_of_classes',
            new_name='number_of_labels',
        ),
    ]
