from django.test import TestCase
from django.conf import settings

from .models import ThreatParameter, PsychWarfareConfig
from .RiotAPI import RiotAPI, SubjectSummoner

import requests
import vcr
import time

# Create your tests here.
class SubjectMethodTests(TestCase):

    def setUp(self):
        """
        Commonly used variables go here
        """
        # This is a bad way to remove sleeps, haven't got mock.patch working yet
        setattr(time, 'sleep', lambda s: None)
        self.dummy_threat_config = ThreatParameter(
            preset_name="Test Threat Default",
            extreme_threat_ratio=60,
            very_high_threat_ratio=55,
            high_threat_ratio=52,
            moderate_threat_ratio=48,
            low_threat_ratio=45,
            very_low_threat_ratio=40
        )
        self.dummy_psych_config = PsychWarfareConfig(
            preset_name="Test Psych Default",
            games_to_fetch=15,
            pattern_extreme=8,
            pattern_high=6,
            pattern_medium=4,
            pattern_low=2,
        )

    @vcr.use_cassette('fixtures/vcr_cassettes/get_summoner_by_name')
    def test_get_summoner_by_name(self):
        dummy_name = 'Aggrastronomer'
        dummy_api = RiotAPI (api_key=settings.RIOT_API_KEY)
        result = dummy_api.get_summoner_by_name(dummy_name)
        self.assertEqual(
            result[dummy_name.lower().replace(" ", "")]['id'],
        22896793)


    @vcr.use_cassette('fixtures/vcr_cassettes/summoner_not_in_game.yaml')
    def test_retrieve_most_played_champion(self):
        """
        Uses dummy data for a summoner not currently in a game
        """
        dummy_summoner = SubjectSummoner(
            summoner_name="Aggrastronomer",
            summoner_riot_id=22896793,
            summoner_level=30,
            psych_war_mod=self.dummy_psych_config,
            threat_config=self.dummy_threat_config
        )
        dummy_summoner.retrieve_most_played_champion()
        self.assertEqual(
            dummy_summoner.most_played_champion_name,
            "Akali",
        )
        self.assertGreaterEqual(
            dummy_summoner.main_win_percentage,
            0,
        )
        self.assertLessEqual(
            dummy_summoner.main_win_percentage,
            100,
        )
        self.assertTrue
        self.assertEqual(
            requests.get(dummy_summoner.most_played_champion_url_splash).status_code,
            200,
        )

    @vcr.use_cassette('fixtures/vcr_cassettes/summoner_is_in_game.yaml')
    def test_retrieve_champion_being_played(self):
        """
        Uses dummy live game data from vcrpy
        """
        dummy_summoner = SubjectSummoner(
            summoner_name="LgnOLl",
            summoner_riot_id=62037423,
            summoner_level=30,
            psych_war_mod=self.dummy_psych_config,
            threat_config=self.dummy_threat_config
        )
        dummy_summoner.retrieve_champion_being_played()
        self.assertEqual(
        len(dummy_summoner.current_game.participants),
        10
        )
        self.assertEqual(
            len(dummy_summoner.current_game.participant_ids),
            10
        )
        self.assertEqual(
            dummy_summoner.current_champion_name,
            "Zyra"
        )
        self.assertEqual(
            dummy_summoner.current_game.predicted_outcome,
            "Team 1"
        )
        self.assertGreaterEqual(
            dummy_summoner.current_game.certainty,
            50
        )
