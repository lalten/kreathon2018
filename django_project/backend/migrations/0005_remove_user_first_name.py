# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-11-24 12:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_container_location_string'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
    ]