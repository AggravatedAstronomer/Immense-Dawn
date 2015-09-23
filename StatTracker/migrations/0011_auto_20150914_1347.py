# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0010_auto_20150904_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='bronze_scrutinised_predictions',
            new_name='bronze_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='challenger_master_scrutinised_predictions',
            new_name='chal_mast_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='challenger_master_success_rating',
            new_name='chal_mast_success_rating',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='challenger_master_successful_predictions',
            new_name='chal_mast_successful_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='diamond_scrutinised_predictions',
            new_name='diamond_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='gold_scrutinised_predictions',
            new_name='gold_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='platinum_scrutinised_predictions',
            new_name='platinum_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='silver_scrutinised_predictions',
            new_name='silver_checked_predictions',
        ),
        migrations.RenameField(
            model_name='selfdiagnosticoverseer',
            old_name='total_scrutinised_predictions',
            new_name='total_checked_predictions',
        ),
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='match_league',
            field=models.CharField(default='League Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='match_result',
            field=models.CharField(default='Result Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='predicted_victor',
            field=models.CharField(default='Inconclusive', max_length=50),
        ),
    ]
