# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 11:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sniff', '0003_auto_20161102_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fb_id',
            new_name='fb_userId',
        ),
    ]
