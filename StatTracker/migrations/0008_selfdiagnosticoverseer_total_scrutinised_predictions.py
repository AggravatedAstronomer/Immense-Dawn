# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0007_selfdiagnosticmodule_match_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='total_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
    ]
