# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20160524_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseinfo',
            name='trans_subtype',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incomeinfo',
            name='trans_subtype',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
    ]
