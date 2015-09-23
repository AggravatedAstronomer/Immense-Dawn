# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0005_auto_20150826_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='total_scrutinised_predictions',
            new_name='bronze_scrutinised_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='success_rating',
            new_name='bronze_success_rating',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='total_successful_predictions',
            new_name='bronze_successful_predictions',
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='challenger_master_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='challenger_master_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='challenger_master_successful_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='diamond_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='diamond_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='diamond_successful_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='gold_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='gold_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='gold_successful_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='platinum_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='platinum_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='platinum_successful_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='silver_scrutinised_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='silver_success_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selfdiagnosticoverseer',
            name='silver_successful_predictions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='name',
            field=models.CharField(default='Self Diagnostic Module', max_length=50),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='level',
            field=models.IntegerField(default=30, editable=False),
        ),
    ]
