# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_customuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='first_name',
            new_name='customer_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
    ]
