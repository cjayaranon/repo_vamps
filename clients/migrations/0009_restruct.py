# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-03 15:01
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_loan_interest_rate_over'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restruct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_in_interest', models.DecimalField(blank=True, decimal_places=1, max_digits=8, validators=[django.core.validators.MinValueValidator(0.1)])),
                ('loan_in_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('loan_over_interest', models.DecimalField(blank=True, decimal_places=1, max_digits=8, validators=[django.core.validators.MinValueValidator(0.1)])),
                ('loan_over_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('loan_root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.loanApplication')),
            ],
        ),
    ]
