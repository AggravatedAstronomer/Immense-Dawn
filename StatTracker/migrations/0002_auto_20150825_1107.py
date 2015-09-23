# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StatTracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfDiagnosticModule',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=25, default='Self Diagnostic Module')),
                ('games_to_store', models.IntegerField(default=50)),
                ('success_rating', models.IntegerField(editable=False, default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='SelfDiagnosticTool',
        ),
    ]
