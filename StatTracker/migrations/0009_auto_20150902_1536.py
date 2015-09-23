# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0008_selfdiagnosticoverseer_total_scrutinised_predictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='total_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='total_successful_predictions',
            field=models.IntegerField(default=0),
        ),
    ]
