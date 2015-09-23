from django.db import models


# Create your models here.
class Summoner(models.Model):
    name = models.CharField(max_length=25)
    riot_id = models.BigIntegerField(default=0, editable=False)
    level = models.IntegerField(default=30, editable=False)
    date_added = models.DateTimeField(("Date"), auto_now_add=True)
    last_check_date = models.DateTimeField(("Date"), auto_now=True)
    career_win_rate = models.IntegerField(default=0, editable=False)
    total_games = models.BigIntegerField(default=0, editable=False)

    def __str__(self):
        return self.name


class ThreatParameter(models.Model):
    date_added = models.DateField(("Date"), auto_now_add=True)
    preset_name = models.CharField(max_length=25, default="Default")
    extreme_threat_ratio = models.IntegerField(default=60)
    very_high_threat_ratio = models.IntegerField(default=55)
    high_threat_ratio = models.IntegerField(default=52)
    moderate_threat_ratio = models.IntegerField(default=48)
    low_threat_ratio = models.IntegerField(default=45)
    very_low_threat_ratio = models.IntegerField(default=40)

    def __str__(self):
        return self.preset_name


class PsychWarfareConfig(models.Model):
    date_added = models.DateField(("Date"), auto_now_add=True)
    preset_name = models.CharField(max_length=25, default="Default")
    games_to_fetch = models.IntegerField(default=15)
    pattern_extreme = models.IntegerField(default=8)
    pattern_high = models.IntegerField(default=6)
    pattern_medium = models.IntegerField(default=4)
    pattern_low = models.IntegerField(default=2)


class SelfDiagnosticModule(models.Model):
    name = models.CharField(max_length=50, default="Self Diagnostic Module")
    analysed_game = models.BigIntegerField(default=0)
    predicted_victor = models.CharField(max_length=50, default="Inconclusive")
    predicted_victor_certainty = models.IntegerField(default=0)
    match_league = models.CharField(max_length=50, default="League Unknown")
    match_result = models.CharField(max_length=50, default="Result Pending")
    prediction_success = models.NullBooleanField()

    def __str__(self):
        return self.name


class SelfDiagnosticOverseer(models.Model):
    name = models.CharField(max_length=30, default="The Diagnostic Overseer")
    bronze_checked_predictions = models.BigIntegerField(default=0)
    bronze_successful_predictions = models.BigIntegerField(default=0)
    bronze_success_rating = models.IntegerField(default=0)
    silver_checked_predictions = models.BigIntegerField(default=0)
    silver_successful_predictions = models.BigIntegerField(default=0)
    silver_success_rating = models.IntegerField(default=0)
    gold_checked_predictions = models.BigIntegerField(default=0)
    gold_successful_predictions = models.BigIntegerField(default=0)
    gold_success_rating = models.IntegerField(default=0)
    platinum_checked_predictions = models.BigIntegerField(default=0)
    platinum_successful_predictions = models.BigIntegerField(default=0)
    platinum_success_rating = models.IntegerField(default=0)
    diamond_checked_predictions = models.BigIntegerField(default=0)
    diamond_successful_predictions = models.BigIntegerField(default=0)
    diamond_success_rating = models.IntegerField(default=0)
    chal_mast_checked_predictions = models.BigIntegerField(default=0)
    chal_mast_successful_predictions = models.BigIntegerField(default=0)
    chal_mast_success_rating = models.IntegerField(default=0)
    total_checked_predictions = models.BigIntegerField(default=0)
    total_successful_predictions = models.BigIntegerField(default=0)
    total_success_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
