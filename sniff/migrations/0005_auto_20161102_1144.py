# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sniff', '0004_auto_20161102_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fb_token',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='user',
            name='fb_userId',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]