# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-07-04 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200703_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websiteinfo',
            name='image',
            field=models.ImageField(blank=True, max_length=256, null=True, upload_to='website_pics'),
        ),
    ]
