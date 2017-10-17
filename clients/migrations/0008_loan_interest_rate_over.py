# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-03 10:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20170831_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='interest_rate_over',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0.1)]),
            preserve_default=False,
        ),
    ]
