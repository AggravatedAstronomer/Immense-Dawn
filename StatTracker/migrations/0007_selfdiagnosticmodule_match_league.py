# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0006_auto_20150902_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='match_league',
            field=models.CharField(max_length=25, default='League Unknown'),
        ),
    ]
