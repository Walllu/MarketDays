# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-18 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0013_item_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='itemDatePosted',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offerTimeStamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='sessionEnd',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='sessionStart',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userStartDate',
            field=models.DateField(auto_now_add=True),
        ),
    ]
