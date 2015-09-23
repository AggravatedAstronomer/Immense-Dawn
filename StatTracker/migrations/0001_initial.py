# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PsychWarfareConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('preset_name', models.CharField(max_length=25, default='Default')),
                ('games_to_fetch', models.IntegerField(default=15)),
                ('pattern_extreme', models.IntegerField(default=8)),
                ('pattern_high', models.IntegerField(default=6)),
                ('pattern_medium', models.IntegerField(default=4)),
                ('pattern_low', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='SelfDiagnosticTool',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('games_to_store', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('riot_id', models.IntegerField(editable=False, default=0)),
                ('level', models.IntegerField(editable=False, default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('last_check_date', models.DateTimeField(verbose_name='Date', auto_now=True)),
                ('career_win_rate', models.IntegerField(editable=False, default=0)),
                ('total_games', models.IntegerField(editable=False, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ThreatParameter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('preset_name', models.CharField(max_length=25, default='Default')),
                ('extreme_threat_ratio', models.IntegerField(default=60)),
                ('very_high_threat_ratio', models.IntegerField(default=55)),
                ('high_threat_ratio', models.IntegerField(default=52)),
                ('moderate_threat_ratio', models.IntegerField(default=48)),
                ('low_threat_ratio', models.IntegerField(default=45)),
                ('very_low_threat_ratio', models.IntegerField(default=40)),
            ],
        ),
    ]
