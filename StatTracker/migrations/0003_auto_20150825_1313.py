# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0002_auto_20150825_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfdiagnosticmodule',
            name='games_to_store',
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='most_recent_prediction',
            field=models.CharField(max_length=25, default='None made'),
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='most_recent_result',
            field=models.CharField(max_length=25, default='Result not retrieved'),
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='most_recent_success',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='most_recently_analysed_game',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='total_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='total_successful_predictions',
            field=models.IntegerField(default=0),
        ),
    ]
