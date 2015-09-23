# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0004_auto_20150825_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfDiagnosticOverseer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(default='The Diagnostic Overseer', max_length=30)),
                ('total_scrutinised_predictions', models.IntegerField(default=0)),
                ('total_successful_predictions', models.IntegerField(default=0)),
                ('success_rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='selfdiagnosticmodule',
            old_name='most_recent_prediction_certainty',
            new_name='analysed_game',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticmodule',
            old_name='most_recent_result',
            new_name='match_result',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticmodule',
            old_name='most_recent_prediction',
            new_name='predicted_victor',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticmodule',
            old_name='most_recently_analysed_game',
            new_name='predicted_victor_certainty',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticmodule',
            old_name='most_recent_success',
            new_name='prediction_success',
        ),
        migrations.RemoveField(
            model_name='selfdiagnosticmodule',
            name='success_rating',
        ),
        migrations.RemoveField(
            model_name='selfdiagnosticmodule',
            name='total_scrutinised_predictions',
        ),
        migrations.RemoveField(
            model_name='selfdiagnosticmodule',
            name='total_successful_predictions',
        ),
    ]
