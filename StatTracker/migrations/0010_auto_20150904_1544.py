# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0009_auto_20150902_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='analysed_game',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='bronze_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='bronze_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='challenger_master_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='challenger_master_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='diamond_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='diamond_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='gold_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='gold_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='platinum_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='platinum_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='silver_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='silver_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='total_scrutinised_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticoverseer',
            name='total_successful_predictions',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='riot_id',
            field=models.BigIntegerField(editable=False, default=0),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='total_games',
            field=models.BigIntegerField(editable=False, default=0),
        ),
    ]
