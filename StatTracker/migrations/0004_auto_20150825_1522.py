# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0003_auto_20150825_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfdiagnosticmodule',
            name='most_recent_prediction_certainty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='selfdiagnosticmodule',
            name='most_recent_prediction',
            field=models.CharField(max_length=25, default='Inconclusive'),
        ),
    ]
