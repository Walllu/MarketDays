# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-10 16:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20180309_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userPhoneNumber',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userStartDate',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
