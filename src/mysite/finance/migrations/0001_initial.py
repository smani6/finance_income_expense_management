# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('tag', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('account_id', models.ForeignKey(to='finance.Account')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('tag', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('account_id', models.ForeignKey(to='finance.Account')),
            ],
        ),
    ]
