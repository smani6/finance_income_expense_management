# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeinfo',
            name='amount',
            field=models.DecimalField(max_digits=11, decimal_places=2),
        ),
    ]
