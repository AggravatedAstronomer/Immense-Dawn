from __future__ import division
from django.conf import settings

import requests

import time
import datetime

from .models import SelfDiagnosticModule

# These functions are used by the SubjectSummoner and Participant objects
class SharedPsychFunctions(object):
    def __init__(self, history, psych_war_mod, riot_id):
        self.api = settings.RIOT_API_KEY
        self.history = history
        self.psych_war_mod = psych_war_mod
        self.riot_id = riot_id
        self.games_to_fetch = self.psych_war_mod.games_to_fetch
        self.match_history = []
        self.recent_wins = 0
        self.recent_losses = 0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.severity_coeff = 0
        self.match_history_debug_message = None
        self.advice = None
        self.psych_core()

    def severity_coefficient(self, x, y, games_to_fetch):
        self.severity_coeff += (
            round(((x - y)**3 / 60**3) * games_to_fetch, 2)
        )
    def normalise_severity_coefficient(self, severity_coefficient):
        if self.severity_coeff < 0:
            self.severity_coeff = -(self.severity_coeff)
        return self.severity_coeff
    def check_for_pattern_reversal(self, pattern, reverse):
        if self.severity_coeff < 0:
            return reverse
        else:
            return pattern

    def psych_core(self):
        if len(self.history['matches']) < self.psych_war_mod.games_to_fetch:
            self.games_to_fetch = len(self.history['matches'])
            self.match_history_debug_message = (
                "Limited history data. \
                        Number of requested games \
                        curtailed to " + str(self.games_to_fetch) + "."
            )

        for i in range(0, self.games_to_fetch):
            root = self.history['matches'][i]
            if root['queue'] == 'RANKED_SOLO_5x5':
                match_id = root['matchId']
                match = RiotAPI(self.api).get_match_by_id(match_id)
                time.sleep(1)
                if match:
                    if len(match['participantIdentities']) != 10:
                        print('DEBUG')
                        print(root['queue'])
                        print(len(match['participantIdentities']))
                    for participant in match['participantIdentities']:
                        print("Participant" + "\n")
                        print(participant)
                        if participant['player']['summonerId'] == self.riot_id:
                            self.participant_id = participant['participantId'] - 1
                    if match['participants'][self.participant_id]['stats']['winner'] is True:
                        self.match_history.append("Win")
                        self.recent_wins += 1
                    else:
                        self.match_history.append("Loss")
                        self.recent_losses += 1
                        
        self.match_history = list(reversed(self.match_history))
        self.recent_win_rate = \
            round((self.recent_wins / self.games_to_fetch) * 100, 2)
        self.recent_loss_rate = \
            round((self.recent_losses / self.games_to_fetch) * 100, 2)

        # Use this match history data to assess the player's psychology
        for i in range(0, len(self.match_history)):
            if self.match_history[i] == "Loss":
                self.consecutive_losses += 1
                self.severity_coeff += 1.0
            else:
                break
        for i in range(0, len(self.match_history)):
            if self.match_history[i] == "Win":
                self.consecutive_wins += 1
                self.severity_coeff += 1.0
            else:
                break
        if self.consecutive_wins != 0:
            self.pattern = "Confident"
            self.consecutive_result = "wins"
            self.consecutive_result_number = self.consecutive_wins
            self.severity_coefficient(
                self.recent_win_rate,
                self.recent_loss_rate,
                self.games_to_fetch
            )
            self.pattern = self.check_for_pattern_reversal(
                self.pattern,
                "Vulnerable"
            )
        elif self.consecutive_losses != 0:
            self.pattern = "Vulnerable"
            self.consecutive_result = "losses"
            self.consecutive_result_number = self.consecutive_losses
            self.severity_coefficient(
                self.recent_loss_rate,
                self.recent_win_rate,
                self.games_to_fetch
            )
            self.pattern = self.check_for_pattern_reversal(
                self.pattern,
                "Confident"
            )
        self.normalise_severity_coefficient(self.severity_coeff)
        if self.severity_coeff >= self.psych_war_mod.pattern_extreme:
            self.severity = "Extreme"
        elif self.severity_coeff >= self.psych_war_mod.pattern_high:
            self.severity = "High"
        elif self.severity_coeff >= self.psych_war_mod.pattern_medium:
            self.severity = "Moderate"
        elif self.severity_coeff >= self.psych_war_mod.pattern_low:
            self.severity = "Low"
        else:
            self.severity = "Minimal"
        if self.severity == "Extreme" or self.severity == "High":
            if self.pattern == "Vulnerable":
                self.advice = "This player is in a negative spiral. \
                    They are probably susceptible to aggressive play styles."
            else:
                self.advice = "Probable dominant behaviour. \
                    A conservative playstyle of defense and economy \
                    is recommended against this player."
        if not self.pattern:
            self.pattern = "Unknown - Data Unavailable"
        if not self.severity:
            self.severity = "Unknown - Data Unavailable"

class SharedThreatFunctions(object):
    def __init__(self, league_win_ratio, threat_config):
        self.league_win_ratio = league_win_ratio
        self.cfg = threat_config
        self.threat_core()

    def threat_core(self):
        if self.league_win_ratio >= self.cfg.extreme_threat_ratio:
            thisThreat = "Extreme"
        elif self.league_win_ratio >= self.cfg.very_high_threat_ratio:
            thisThreat = "Very High"
        elif self.league_win_ratio >= self.cfg.high_threat_ratio:
            thisThreat = "High"
        elif self.league_win_ratio >= self.cfg.moderate_threat_ratio:
            thisThreat = "Moderate"
        elif self.league_win_ratio >= self.cfg.low_threat_ratio:
            thisThreat = "Low"
        elif self.league_win_ratio >= self.cfg.very_low_threat_ratio:
            thisThreat = "Very Low"
        else:
            thisThreat = "Minimal"
        self.rating = thisThreat


class RiotAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.region = settings.RIOT_REGIONS['europe_west']

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            settings.RIOT_URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url
                ),
            params=args
            )
        if response.status_code != 200:
            return None

        print(response.url)
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = settings.RIOT_URL['summoner_by_name'].format(
            version=settings.RIOT_API_VERSIONS['summoner'],
            names=name
            )
        return self._request(api_url)

    def get_stats_by_id(self, riot_id):
        api_url = settings.RIOT_URL['stats_by_id'].format(
            version=settings.RIOT_API_VERSIONS['stats'],
            summoner_id=riot_id,
            year=datetime.date.today().year
            )
        return self._request(api_url)

    def get_league_by_id(self, riot_id):
        api_url = settings.RIOT_URL['league_by_id'].format(
            version=settings.RIOT_API_VERSIONS['league'],
            summoner_id=riot_id
            )
        return self._request(api_url)

    def get_history_by_id(self, riot_id, psych_war_mod):
        gamesToFetch = psych_war_mod.games_to_fetch
        api_url = settings.RIOT_URL['match_history_by_id'].format(
            version=settings.RIOT_API_VERSIONS['match_history'],
            summoner_id=riot_id,
            begin=0,
            end=gamesToFetch
            )
        return self._request(api_url)

    def get_match_by_id(self, match_id):
        api_url = settings.RIOT_URL['match_by_id'].format(
            version=settings.RIOT_API_VERSIONS['match'],
            match_id=match_id
            )
        return self._request(api_url)

    def get_current_game_by_id(self, riot_id, params={}):
        """ this function does stuff """
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            settings.RIOT_URL['current_game_by_id'].format(
                region=self.region,
                platformId="EUW1",
                summoner_id=riot_id
                ),
            params=args
            )
        if response.status_code != 200:
            return None

        print(response.url)
        return response.json()

    def get_featured_games(self, params={}):
        """ this function does stuff """
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            settings.RIOT_URL['featured_games'].format(
                region=self.region
                ),
            params=args
            )
        if response.status_code != 200:
            return None

        print(response.url)
        return response.json()

    def get_game_version(self, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            settings.RIOT_URL['version_by_region'].format(
                region=self.region,
                version=settings.RIOT_API_VERSIONS['static_data']
                ),
            params=args
            )
        if response.status_code != 200:
            return None

        print(response.url)
        return response.json()

    def get_champion_list(self, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            settings.RIOT_URL['champion_list'].format(
                region=self.region,
                version=settings.RIOT_API_VERSIONS['static_data'],
                ),
            params=args
            )
        if response.status_code != 200:
            return None

        print(response.url)
        return response.json()


class ChampionImagesFactory(object):

    def __init__(self, champ_master_list, game_version):
        self.champ_master_list = champ_master_list
        self.game_version = game_version

    def get_champ(self, champ_id):
        return ChampionImages(self, champ_id)


class ChampionImages(object):

    # These images are used by the subject summoner and participants
    BASE_IMG_URL = "http://ddragon.leagueoflegends.com/cdn"
    SPLASH_IMG_URL = BASE_IMG_URL + "/img/champion/splash/{name}_0.jpg"
    LOADING_IMG_URL = BASE_IMG_URL + "/img/champion/loading/{name}_0.jpg"
    SQUARE_IMG_URL = BASE_IMG_URL + "/{game_version}/img/champion/{name}.png"

    def __init__(self, factory, champ_id):
        self.factory = factory
        self.champ_id = str(champ_id)

    @property
    def key(self):
        return self.factory.champ_master_list[self.champ_id]['key']

    @property
    def splash(self):
        return self.SPLASH_IMG_URL.format(
            name=self.key
        )

    @property
    def loading(self):
        return self.LOADING_IMG_URL.format(
            name=self.key
        )

    @property
    def square(self):
        return self.SQUARE_IMG_URL.format(
            name=self.key,
            game_version=self.factory.game_version
        )


class IndexListScanner(object):
    """
    Determines whether summoners in a list are in a game, and what type
    """
    def __init__(self, riot_id):
        self.api = settings.RIOT_API_KEY
        self.riot_id = riot_id

    def scan_list_for_ranked_game_in_progress(self):
        self.game_state = \
            RiotAPI(self.api).get_current_game_by_id(self.riot_id)
        if self.game_state:
            if self.game_state['gameType'] == 'MATCHED_GAME':
                if self.game_state['gameQueueConfigId'] == 4:
                    self.game_id = self.game_state['gameId']
                    return True


class ErrorHandler(object):
    """
    Determines when errors will appear to guide the user
    """
    def __init__(self, summoner_name):
        self.summoner_name = summoner_name
        self.summoner_not_exist = False

class SubjectSummoner(object):
    """
    Describes the specific summoner (player) being indexed
    """
    def __init__(self, summoner_name, summoner_riot_id, summoner_level,
                 psych_war_mod, threat_config):
        self.api = RiotAPI(settings.RIOT_API_KEY)
        self.name = summoner_name.lower().replace(" ", "")
        self.psych_war_mod = psych_war_mod
        self.threat_config = threat_config
        self.display_name = summoner_name
        self.riot_id = summoner_riot_id
        self.level = summoner_level
        # Get up to date champion static data
        self.champ_master_list = self.api.get_champion_list()
        if self.champ_master_list is not None:
            self.champ_master_list = self.champ_master_list['data']
        # Retrieve current game version number
        self.game_version = self.api.get_game_version()
        if self.game_version is not None:
            self.game_version = self.game_version[0]
        else:
            self.game_version = "5.18.1"
        print("Current Game Version for EUW: " + self.game_version)
        # Hence create an image handler object for existing champions
        self.image_handler = ChampionImagesFactory(
            self.champ_master_list,
            self.game_version
        )
        # Make API requests using summoner's unique riot ID
        self.ranked_data = \
            self.api.get_stats_by_id(self.riot_id)
        time.sleep(1)
        self.league_data = \
            self.api.get_league_by_id(self.riot_id)
        time.sleep(1)
        self.history_data = \
            self.api.get_history_by_id(self.riot_id, self.psych_war_mod)

        # Retrieve data from all returned API json output
        if self.ranked_data:
            self.retrieve_ranked_stats()
            self.retrieve_most_played_champion()
        if self.league_data:
            self.retrieve_league_stats()
        if self.history_data:
            self.retrieve_match_history()
        # Get data about the current game if one is in progress
        self.current_game = Game(
            self.riot_id,
            self.psych_war_mod,
            self.threat_config,
            self.champ_master_list,
            self.game_version
        )
        time.sleep(1)
        if self.current_game.game_data:
            self.retrieve_champion_being_played()

    def retrieve_ranked_stats(self):
        """
        Retrieves the ranked stats of the player from the stats api
        """
        for key in self.ranked_data['champions']:
            if key['id'] == 0:
                root = key['stats']
                self.total_doubles = root['totalDoubleKills']
                self.total_triples = root['totalTripleKills']
                self.total_quadras = root['totalQuadraKills']
                self.total_pentas = root['totalPentaKills']
                self.largest_killing_spree = root['maxLargestKillingSpree']
                self.max_champions_killed = root['mostChampionKillsPerSession']
                self.total_turrets_killed = root['totalTurretsKilled']
                self.total_sessions_won = root['totalSessionsWon']
                self.total_sessions_lost = root['totalSessionsLost']
                self.total_games = root['totalSessionsPlayed']
                self.career_win_rate = (
                    round((self.total_sessions_won / self.total_games)
                          * 100, 2)
                )
                self.total_champions_killed = root['totalChampionKills']

    def retrieve_league_stats(self):
        """
        Retrieves league and division stats from the api
        """
        self.league_win_ratio = False
        cfg = self.threat_config
        for key in self.league_data:
            if self.league_data[key][0]['queue'] != 'RANKED_SOLO_5x5':
                continue
            entries = self.league_data[key][0]['entries']
            self.tier = self.league_data[key][0]['tier']
            self.queue_type = "Ranked 5v5"
            self.league_and_division = self.tier + " " + entries[0]['division']
            self.ladder_points = entries[0]['leaguePoints']
            self.hot_streak = entries[0]['isHotStreak']
            self.veteran_status = entries[0]['isVeteran']
            self.league_wins = entries[0]['wins']
            self.league_losses = entries[0]['losses']
            self.league_win_ratio = (
                round((self.league_wins / (self.league_wins +
                                           self.league_losses))*100, 2)
            )
        if self.league_win_ratio is not False:
            threat_assessment = SharedThreatFunctions(
                self.league_win_ratio,
                cfg,
            )
            self.threat_rating = threat_assessment.rating
        else:
            self.threat_rating = "No league data exists yet"

    def retrieve_match_history(self):
        """
        Gets recent match history from the api, predicts psychology
        """
        if self.history_data is not None:
            psych_evaluation = SharedPsychFunctions(
                self.history_data,
                self.psych_war_mod,
                self.riot_id
            )
            self.match_history = psych_evaluation.match_history
            self.consecutive_result = psych_evaluation.consecutive_result
            self.consecutive_result_number = \
                psych_evaluation.consecutive_result_number
            self.pattern = psych_evaluation.pattern
            self.severity = psych_evaluation.severity
            if psych_evaluation.match_history_debug_message is not None:
                self.match_history_debug_message = \
                    psych_evaluation.match_history_debug_message
            self.games_to_fetch = psych_evaluation.games_to_fetch
            self.recent_win_rate = psych_evaluation.recent_win_rate
            self.advice = psych_evaluation.advice


    def retrieve_most_played_champion(self):
        champions_played = {}
        self.champ_master_list
        for key in self.ranked_data['champions']:
            if key['id'] == 0:
                continue
            games_played = key['stats']['totalSessionsPlayed']
            champion_id = key['id']
            champions_played[champion_id] = games_played
        most_games = max(champions_played.values())
        for key in self.ranked_data['champions']:
            if key['stats']['totalSessionsPlayed'] != most_games:
                continue
            most_played_champion_id = key['id']
        self.most_played_champion_name = \
            self.champ_master_list[str(most_played_champion_id)]['name']
        self.most_played_champion_title = \
            self.champ_master_list[str(most_played_champion_id)]['title']
        images = self.image_handler.get_champ(most_played_champion_id)
        self.most_played_champion_url_splash = images.splash
        self.most_played_champion_url = images.loading
        self.most_played_champion_square_url = images.square
        for key in self.ranked_data['champions']:
            if key['id'] != most_played_champion_id:
                continue
            root = key['stats']
            self.main_doubles = root['totalDoubleKills']
            self.main_triples = root['totalTripleKills']
            self.main_quadras = root['totalQuadraKills']
            self.main_pentas = root['totalPentaKills']
            self.main_most_champions_killed = (
                root['mostChampionKillsPerSession'])
            self.main_turrets_killed = root['totalTurretsKilled']
            self.main_sessions_won = root['totalSessionsWon']
            self.main_sessions_lost = root['totalSessionsLost']
            self.main_sessions_played = root['totalSessionsPlayed']
            self.main_win_percentage = (
                round((self.main_sessions_won / self.main_sessions_played)
                      * 100, 2)
            )
            self.main_champions_killed = root['totalChampionKills']

    def retrieve_champion_being_played(self):
        """
        Retrieves the player's stats with the currently played champion
        """
        game = self.current_game.game_data
        participants = game['participants']
        for participant in participants:
            if participant['summonerName'] != self.display_name:
                continue
            self.current_champion_id = participant['championId']
            self.current_champion_name = \
                self.champ_master_list[str(self.current_champion_id)]['name']
            self.current_champion_title = \
                self.champ_master_list[str(self.current_champion_id)]['title']
            images = self.image_handler.get_champ(self.current_champion_id)
            self.champion_url_splash = images.splash
            self.champion_url = images.loading
            self.champion_square_url = images.square
        if self.ranked_data is None:
            return
        for key in self.ranked_data['champions']:
            if key['id'] == self.current_champion_id:
                root = key['stats']
                self.current_champion_doubles = (
                    root['totalDoubleKills'])
                self.current_champion_triples = (
                    root['totalTripleKills'])
                self.current_champion_quadras = (
                    root['totalQuadraKills'])
                self.current_champion_pentas = (
                    root['totalPentaKills'])
                self.current_champion_max_kills = (
                    root['mostChampionKillsPerSession'])
                self.current_champion_total_turrets_killed = (
                    root['totalTurretsKilled'])
                self.current_champion_total_sessions_won = (
                    root['totalSessionsWon'])
                self.current_champion_total_sessions_lost = (
                    root['totalSessionsLost'])
                self.current_champion_total_sessions_played = (
                    root['totalSessionsPlayed'])
                x = self.current_champion_total_sessions_won
                y = self.current_champion_total_sessions_played
                self.current_champion_career_win_percentage = (
                    round((x / y) * 100, 2))
                self.current_champion_total_champions_killed = (
                    root['totalChampionKills'])


class Game(object):
    """
    Describes the game
    """
    def __init__(self, riot_id, psych_war_mod, threat_config,
                 champ_master_list, game_version):
        # Get game json
        self.api = RiotAPI(settings.RIOT_API_KEY)
        self.game_data = self.api.get_current_game_by_id(riot_id)
        self.psych_war_mod = psych_war_mod
        self.threat_config = threat_config
        self.participants = []
        self.participant_ids = []
        self.teams = []
        self.champ_master_list = champ_master_list
        self.game_version = game_version
        self.image_handler = ChampionImagesFactory(
            self.champ_master_list,
            self.game_version
        )

        if self.game_data:
            self.game_id = self.game_data['gameId']
            self.populate_participants()
            if self.game_data['gameQueueConfigId'] == 4:
                self.display_table = True
                self.predict_outcome()

    def populate_participants(self):
        """
        Instantiates the participant list
        """
        # Unlike the Match History and Stats api requests, the league
        # api request supports a list of 10 IDs, so we use this to save
        # 9 api requests
        for i in range(0, len(self.game_data['participants'])):
            self.participant_ids.append(
                self.game_data['participants'][i]['summonerId']
            )

        self.participant_ids_query_string = \
            str(self.participant_ids).replace("[", "").replace("]", "")
        self.league_data_all_players = \
            self.api.get_league_by_id(self.participant_ids_query_string)
        time.sleep(1)
        participant_number = 0

        for participant_data in self.game_data['participants']:
            participant_number += 1
            images = \
                self.image_handler.get_champ(participant_data['championId'])
            participant_data['splash_url'] = images.splash
            participant_data['loading_url'] = images.loading
            participant_data['square_url'] = images.square
            self.participants.append(Participant(
                participant_number,
                self.psych_war_mod,
                self.threat_config,
                self.league_data_all_players,
                self.champ_master_list,
                game=self,
                data=participant_data
            ))
            time.sleep(5)

    def game_type(self):
        """
        Retrieves the game type from the current game api
        """
        if self.game_data:
            if self.game_data['gameQueueConfigId'] == 4:
                return "In a Ranked 5v5 Game"
            else:
                return "In a Non-Ranked Game"
        else:
            return "Not in a Game"

    def predict_outcome(self):
        """
        Predicts the outcome of the game based on gathered team stats.

        Based on the stats for win rate with current champion and
        psychological state derived from recent match history,
        quantifies the advantages, predicts the game outcome, and
        provides an estimate for the associated probability.
        """

        if self.game_data['gameQueueConfigId'] != 4:
            return None
        self.certainty = None
        for i in range(0, 2):
            self.teams.append(Team(number=i+1))
        for participant in self.participants:
            print("Analysing " + participant.summoner_name)

            # The team numbers are 1 and 2, the team[] indices are
            # 0 and 1, so subtract one here.
            team_number = int(participant.team) - 1
            team_num = self.teams[team_number]

            # Aggregate champion skill
            if participant.win_rate_obtained:
                team_num.total_win += participant.champion_win_rate
            elif participant.stats is not None:
                team_num.total_win += 25
            else:
                team_num.total_win += 50

            # Aggregate overall threat level
            team_num.total_threat += participant.league_win_ratio

            # Aggregate and quantify morale
            if participant.pattern == ("Unknown - Data Unavailable"):
                team_num.total_morale += 50
            elif participant.severity == ("Unknown - Data Unavailable"):
                team_num.total_morale += 50
            elif (participant.severity == "Extreme" and
                  participant.pattern == "Confident"):
                team_num.total_morale += 100
            elif (participant.severity == "High" and
                  participant.pattern == "Confident"):
                team_num.total_morale += 90
            elif (participant.severity == "Moderate" and
                  participant.pattern == "Confident"):
                team_num.total_morale += 80
            elif (participant.severity == "Low" and
                  participant.pattern == "Confident"):
                team_num.total_morale += 70
            elif (participant.severity == "Minimal" and
                  participant.pattern == "Confident"):
                team_num.total_morale += 60
            elif (participant.severity == "Extreme" and
                  participant.pattern == "Vulnerable"):
                team_num.total_morale += 0
            elif (participant.severity == "High" and
                  participant.pattern == "Vulnerable"):
                team_num.total_morale += 10
            elif (participant.severity == "Moderate" and
                  participant.pattern == "Vulnerable"):
                team_num.total_morale += 20
            elif (participant.severity == "Low" and
                  participant.pattern == "Vulnerable"):
                team_num.total_morale += 30
            elif (participant.severity == "Minimal" and
                  participant.pattern == "Vulnerable"):
                team_num.total_morale += 40

        # Average champion win rates
        self.team1_average_champion_winrate = \
            round(self.teams[0].total_win / 5, 2)
        self.team2_average_champion_winrate = \
            round(self.teams[1].total_win / 5, 2)

        # Average threat level
        self.team1_average_threat = \
            round(self.teams[0].total_threat / 5, 2)
        self.team2_average_threat = \
            round(self.teams[1].total_threat / 5, 2)

        # Average morale ratings
        self.team1_average_morale = round(self.teams[0].total_morale / 5, 2)
        self.team2_average_morale = round(self.teams[1].total_morale / 5, 2)

        # Win rate analysis
        av_wr = [self.team1_average_champion_winrate,
                 self.team2_average_champion_winrate]
        self.skill_difference = round(max(av_wr) - min(av_wr), 1)
        if self.skill_difference == 0:
            self.higher_skill_team = \
                "Average champion win rate is equal for both teams"
            self.skill_difference = "None"
            self.equal_skill = True
        else:
            for i in range(0, len(self.teams)):
                if max(av_wr) == av_wr[i]:
                    self.higher_skill_team = self.teams[i].name
                    self.teams[i].total_advantage += self.skill_difference

        # Threat analysis
        av_tr = [self.team1_average_threat,
                  self.team2_average_threat]
        self.threat_difference = round(max(av_tr) - min(av_tr), 1)
        if self.threat_difference == 0:
            self.higher_threat_team = \
                "Average threat rating is equal for both teams"
            self.threat_difference = "None"
            self.equal_threat = True
        else:
            for i in range(0, len(self.teams)):
                if max(av_tr) == av_tr[i]:
                    self.higher_threat_team = self.teams[i].name
                    self.teams[i].total_advantage += self.threat_difference

        # Morale analysis
        av_mo = [self.team1_average_morale, self.team2_average_morale]
        self.morale_difference = round(max(av_mo) - min(av_mo), 1)
        if self.morale_difference == 0:
            self.higher_morale_team = \
                "Projected morale is equal for both teams"
            self.morale_difference = "None"
            self.equal_morale = True
        else:
            for i in range(0, len(self.teams)):
                if max(av_mo) == av_mo[i]:
                    self.higher_morale_team = self.teams[i].name
                    self.teams[i].total_advantage += self.morale_difference

        # Overall advantage analysis and outcome prediction
        advantage_scores = [self.teams[0].total_advantage,
                            self.teams[1].total_advantage]

        for i in range(0,len(self.teams)):
            print(self.teams[i].name)
            print(self.teams[i].total_win)
            print(self.teams[i].total_threat)
            print(self.teams[i].total_morale)
            print(self.teams[i].total_advantage)

        self.total_advantage_difference = \
            round(max(advantage_scores) - min(advantage_scores), 1)

        if self.total_advantage_difference > 12:
            for i in range(0, len(advantage_scores)):
                if max(advantage_scores) == advantage_scores[i]:
                    self.predicted_outcome = self.teams[i].name
                    self.certainty = \
                        round(50 + (self.total_advantage_difference / 6), 1)
                    print(self.predicted_outcome)
                    print(self.certainty)
        else:
            self.predicted_outcome = "Inconclusive"
            self.inconclusive = True


class Team(object):
    def __init__(self, number):
        self.number = number
        self.name = "Team " + str(self.number)
        self.total_win = 0
        self.total_threat = 0
        self.total_morale = 0
        self.total_advantage = 0


class Participant(object):
    """
    Describes a participant in the game
    """
    def __init__(self, participant_number, psych_war_mod, threat_config,
                 league_data_all_players, champ_master_list,
                 game=None, data=None):
        self.api = RiotAPI(settings.RIOT_API_KEY)
        self.pattern = ""
        self.severity = ""
        self.data = data
        self.game = game
        self.psych_war_mod = psych_war_mod
        self.threat_config = threat_config
        self.summoner_name = data['summonerName']
        self.riot_id = data['summonerId']
        self.team = str((data['teamId']))[:1]
        self.number = participant_number
        if self.number == 1:
            self.first_participant = True
        if self.number == 5:
            self.divider_participant = True
        self.champion_id = self.data['championId']

        self.champion_name = champ_master_list[str(self.champion_id)]['name']
        self.champion_title = champ_master_list[str(self.champion_id)]['title']
        self.icon_url = self.data['square_url']
        wiki_url = "http://leagueoflegends.wikia.com/wiki/{champ}"
        self.wiki_url = wiki_url.format(champ=self.champion_name)
        self.win_rate_obtained = False
        self.stats = self.api.get_stats_by_id(self.riot_id)
        self.league_data_all_players = league_data_all_players
        self.league = {}
        for key in self.league_data_all_players:
            league_root = self.league_data_all_players[key][0]
            if league_root['queue'] == "RANKED_SOLO_5x5":
                name = league_root['entries'][0]['playerOrTeamName']
                if name == self.summoner_name:
                    self.league = league_root
        self.history = self.api.get_history_by_id(
            self.riot_id,
            self.psych_war_mod
        )
        time.sleep(1)
        self.retrieve_champion_win_rate()
        self.psych_state()
        self.threat()

    def retrieve_champion_win_rate(self):
        print("Harvesting API data for " + self.summoner_name)
        if self.stats is not None:
            for key in self.stats['champions']:
                if key['id'] == self.champion_id:
                    stats = key['stats']
                    self.champion_wins = stats['totalSessionsWon']
                    self.champion_games = stats['totalSessionsPlayed']
                    self.champion_win_rate = int(
                        round((self.champion_wins / self.champion_games)
                              * 100, 0)
                    )
                    self.win_rate_obtained = True
            if not self.win_rate_obtained:
                self.champion_win_rate = "Champion not played in ranked"
        else:
            self.champion_win_rate = "Failure to retrieve ranked stats"

    def threat(self):
        if self.league != {}:
            self.league_data = self.league['entries']
            wins = self.league_data[0]['wins']
            losses = self.league_data[0]['losses']
            if wins + losses > 0:
                self.league_win_ratio = round(wins / (wins + losses) * 100, 2)
            else:
                self.league_win_ratio = 50
            threat_assessment = SharedThreatFunctions(
                self.league_win_ratio,
                self.threat_config
            )
            self.threat_rating = threat_assessment.rating
            tier = self.league['tier']
            division = self.league_data[0]['division']
            self.league_and_division = tier + " " + division
        else:
            self.threat_failed = True
            self.threat_error_message = \
                "League data unavailable for this player"

    def psych_state(self):
        """
        Uses the same functionality as the SubjectSummoner to assess
        psychology of the Participant
        """
        if self.history is not None:
            psych_evaluation = SharedPsychFunctions(
                self.history,
                self.psych_war_mod,
                self.riot_id
            )
            self.pattern = psych_evaluation.pattern
            self.severity = psych_evaluation.severity
        else:
            self.pattern = "Unknown - Data Unavailable"
            self.severity = "Unknown - Data Unavailable"
