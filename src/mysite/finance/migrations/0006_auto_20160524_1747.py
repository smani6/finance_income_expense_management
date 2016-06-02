# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20160524_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='created_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='modified_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='modified_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='expenseinfo',
            name='created_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='expenseinfo',
            name='created_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='expenseinfo',
            name='modified_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='expenseinfo',
            name='modified_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='incomeinfo',
            name='created_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='incomeinfo',
            name='created_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='incomeinfo',
            name='modified_by',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='incomeinfo',
            name='modified_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
