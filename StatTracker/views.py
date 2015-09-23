from __future__ import division
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db import models

import time

from django.conf import settings

from .models import (
    Summoner, ThreatParameter, PsychWarfareConfig, SelfDiagnosticModule, SelfDiagnosticOverseer
)
from .RiotAPI import (
    RiotAPI, SubjectSummoner, IndexListScanner, ErrorHandler
)
import random

def index(request):
    summoner_list = Summoner.objects.order_by('-last_check_date')[:]
    in_ranked_game_list = []
    threat_list = ThreatParameter.objects.order_by('preset_name')[:]
    psych_list = PsychWarfareConfig.objects.order_by('preset_name')[:]
    diagnostic_list = SelfDiagnosticModule.objects.order_by('pk')[:]
    api = RiotAPI(settings.RIOT_API_KEY)
    summoner_name = request.GET.get('name')
    threat_config = request.GET.get('threat_quotient')
    psych_config = request.GET.get('psych_war')
    summoner_core_info = api.get_summoner_by_name(summoner_name)
    error = request.GET.get('error')
    if not error:
        error = ErrorHandler(summoner_name)

    for self_diagnostic in diagnostic_list:
        if self_diagnostic.match_result == "Result Pending":
            if self_diagnostic.predicted_victor != "Inconclusive":
                subject_game = api.get_match_by_id(self_diagnostic.analysed_game)
                if subject_game is not None:
                    if self_diagnostic.predicted_victor == "Team 1":
                        winning_team = 0
                    if self_diagnostic.predicted_victor == "Team 2":
                        winning_team = 1
                    for j in range(0,2):
                        if subject_game['teams'][j]['winner'] == True:
                            self_diagnostic.match_result = "Team " + str(j+1)
                            print(winning_team)
                            print(subject_game['teams'][j])
                            if j == winning_team:
                                self_diagnostic.prediction_success = True
                            else:
                                self_diagnostic.prediction_success = False
                    self_diagnostic.save()
    overseer = SelfDiagnosticOverseer.objects.get(pk=1)
    for self_diagnostic in diagnostic_list:
        if self_diagnostic.prediction_success == True:
            if self_diagnostic.match_league == "BRONZE":
                overseer.bronze_successful_predictions += 1
            elif self_diagnostic.match_league == "SILVER":
                overseer.silver_successful_predictions += 1
            elif self_diagnostic.match_league == "GOLD":
                overseer.gold_successful_predictions += 1
            elif self_diagnostic.match_league == "PLATINUM":
                overseer.platinum_successful_predictions += 1
            elif self_diagnostic.match_league == "DIAMOND":
                overseer.diamond_successful_predictions += 1
            elif self_diagnostic.match_league == "MASTER" or \
                 self_diagnostic.match_league == "CHALLENGER":
                overseer.chal_mast_successful_predictions += 1
            overseer.total_successful_predictions += 1
        if self_diagnostic.prediction_success is not None:
            if self_diagnostic.match_league == "BRONZE":
                overseer.bronze_checked_predictions += 1
            elif self_diagnostic.match_league == "SILVER":
                overseer.silver_checked_predictions += 1
            elif self_diagnostic.match_league == "GOLD":
                overseer.gold_checked_predictions += 1
            elif self_diagnostic.match_league == "PLATINUM":
                overseer.platinum_checked_predictions += 1
            elif self_diagnostic.match_league == "DIAMOND":
                overseer.diamond_checked_predictions += 1
            elif self_diagnostic.match_league == "MASTER" or \
                 self_diagnostic.match_league == "CHALLENGER":
                overseer.chal_mast_checked_predictions += 1
            overseer.total_checked_predictions += 1
            self_diagnostic.delete()
    if overseer.bronze_checked_predictions > 0:
        overseer.bronze_success_rating = round((overseer.bronze_successful_predictions / overseer.bronze_checked_predictions) * 100, 2)
    if overseer.silver_checked_predictions > 0:
        overseer.silver_success_rating = round((overseer.silver_successful_predictions / overseer.silver_checked_predictions) * 100, 2)
    if overseer.gold_checked_predictions > 0:
        overseer.gold_success_rating = round((overseer.gold_successful_predictions / overseer.gold_checked_predictions) * 100, 2)
    if overseer.platinum_checked_predictions > 0:
        overseer.platinum_success_rating = round((overseer.platinum_successful_predictions / overseer.platinum_checked_predictions) * 100, 2)
    if overseer.diamond_checked_predictions > 0:
        overseer.diamond_success_rating = round((overseer.diamond_successful_predictions / overseer.diamond_checked_predictions) * 100, 2)
    if overseer.chal_mast_checked_predictions > 0:
        overseer.chal_mast_success_rating = round((overseer.chal_mast_successful_predictions / overseer.chal_mast_checked_predictions) * 100, 2)
    if overseer.total_checked_predictions > 0:
        overseer.total_success_rating = round((overseer.total_successful_predictions / overseer.total_checked_predictions) * 100, 2)
    overseer.save()
    diagnostic_list = SelfDiagnosticModule.objects.order_by('pk')[:]
    overseer.pending_games = len(diagnostic_list)

    ranked_games_already_found = []
    def find_games(start_point):
        for summoner in summoner_list[start_point:100:10]:
            time.sleep(1)
            print("Querying " + summoner.name)
            index_scanner = IndexListScanner(summoner.riot_id)
            summoner.game = \
                index_scanner.scan_list_for_ranked_game_in_progress()
            if summoner.game:
                if index_scanner.game_id not in ranked_games_already_found:
                    in_ranked_game_list.append(summoner)
                    ranked_games_already_found.append(index_scanner.game_id)
    find_games(0)

    in_ranked_game_list = in_ranked_game_list[:10]
    recent_summoner_list = summoner_list[:10]

    context = RequestContext(request, {
        'summoner_list': summoner_list,
        'recent_summoner_list': recent_summoner_list,
        'in_ranked_game_list': in_ranked_game_list,
        'threat_quotient_parameter_list': threat_list,
        'psych_war_module_list': psych_list,
        'error_handler': error,
        'overseer': overseer
    })
    # Temporary looping code to allow automatic data gathering. Comment this
    """
    render(request, 'StatTracker/index.html', context)
    time.sleep(10)
    temp_summoner = in_ranked_game_list[int(random.randrange(0,9))]
    return HttpResponseRedirect("/summoner/?threat_quotient=1&psych_war=1" + 
                                "&summoner_id={sum_id}".format(
                                    sum_id=temp_summoner.id)
                                )
    """
    # Temporary looping code ends
    return render(request, 'StatTracker/index.html', context)


def detail(request, summoner_id=None):

    if not summoner_id:
        summoner_id = request.GET.get('summoner_id')
    summoner = get_object_or_404(Summoner, pk=summoner_id)
    threat_quotient_parameter_id = request.GET.get('threat_quotient', 1)
    psych_war_module_id = request.GET.get('psych_war', 1)
    threat_config = get_object_or_404(
        ThreatParameter, pk=threat_quotient_parameter_id)
    psych_war_mod = get_object_or_404(
        PsychWarfareConfig, pk=psych_war_module_id)
    diagnostic_name_str = "Diagnostic Module - Caretaker for game {game_id}"

    subject = SubjectSummoner(
        summoner.name,
        summoner.riot_id,
        summoner.level,
        psych_war_mod,
        threat_config
    )

    riot_id = subject.riot_id
    current_game = subject.current_game
    ranked_stats = subject.ranked_data
    league_stats = subject.league_data

    # Check if summoner is able to play ranked
    if subject.level != 30:
        summoner.last_check_date = models.DateField("Date")
        return HttpResponse(
            "This summoner is only level " + str(subject.level) +
            " and therefore not eligible for ranked games.")

    # Store some stats in the summoner object for display at index
    if ranked_stats is not None:
        summoner.total_games = subject.total_games
        summoner.career_win_rate = subject.career_win_rate

    # See if summoner is currently assigned to a league/division
    if league_stats is not None:
        for key in league_stats:
            root = league_stats[key][0]
            if (root['queue']) != 'RANKED_SOLO_5x5':
                summoner.last_check_date = models.DateField("Date")
                return HttpResponse(
                    "This summoner is level 30 but has not completed their "
                    "ranked placement matches.")
    else:
        summoner.last_check_date = models.DateField("Date")
        return HttpResponse("Error: League stats unavailable. " +
                            "Probable causes: This summoner is level " +
                            "30 but has not completed their ranked" +
                            "placement matches. The League API is " +
                            "down or not responding.")

    if current_game.game_data is not None:
        if current_game.game_data['gameQueueConfigId'] == 4:
            game_already_analysed = None
            diagnostic_list = SelfDiagnosticModule.objects.order_by('pk')[:]
            for self_diagnostic in diagnostic_list:
                if self_diagnostic.analysed_game == current_game.game_id:
                    game_already_analysed = True
                    break
            if game_already_analysed is not True:
                if current_game.predicted_outcome is not "Inconclusive":
                    self_diagnostic = SelfDiagnosticModule(
                        name=diagnostic_name_str.format(
                            game_id=current_game.game_id
                        )
                    )
                    self_diagnostic.analysed_game = current_game.game_id
                    print(str(self_diagnostic) + ": Initialised")
                    self_diagnostic.match_result = "Result Pending"
                    self_diagnostic.prediction_success = None
                    if current_game.certainty is not None:
                        self_diagnostic.predicted_victor_certainty = \
                            current_game.certainty
                    self_diagnostic.predicted_victor = \
                        current_game.predicted_outcome
                    self_diagnostic.match_league = subject.tier
                    self_diagnostic.save()

    context = RequestContext(request, {
        'summoner': summoner,
        'subject': subject,
        'threat_config': threat_config,
        'psych_war_mod': psych_war_mod,
        'current_game': current_game
    })
    # Update the summoner object in the database
    summoner.riot_id = riot_id
    summoner.save()

    summoner_list = Summoner.objects.order_by('-last_check_date')[:]
    existing_summoners = []
    for summoner in summoner_list:
        existing_summoners.append(summoner.name)
    for participant in current_game.participants:
        if participant.summoner_name in existing_summoners:
            continue
        else:
            participant = Summoner(
                name=participant.summoner_name,
                riot_id=participant.riot_id,
            )
            participant.save()
    # Temporary code to allow automatic data gathering
    """
    render(request, 'StatTracker/detail.html', context)
    time.sleep(10)
    return HttpResponseRedirect("/")
    """
    # Temporary code ends
    """
    # Temporary code to allow automatic looking up of featured games
    time.sleep(10)
    return HttpResponseRedirect('/')
    """
    return render(request, 'StatTracker/detail.html', context)

def search_summoner(request, summoner_name=None):
    print("Hit the view")
    if not summoner_name:
        summoner_name = request.GET.get('name')
    api = RiotAPI(settings.RIOT_API_KEY)
    print(summoner_name)
    threat_quotient_parameter_id = request.GET.get('threat_quotient', 1)
    psych_war_module_id = request.GET.get('psych_war', 1)
    threat_config = get_object_or_404(
        ThreatParameter, pk=threat_quotient_parameter_id)
    psych_config = get_object_or_404(
        PsychWarfareConfig, pk=psych_war_module_id)
    summoner_core_info = api.get_summoner_by_name(summoner_name)
    summoner_list = Summoner.objects.order_by('-last_check_date')[:]
    error = ErrorHandler(
        summoner_name=summoner_name
    )
    
    if summoner_name:
        if summoner_core_info:
            print("Got Summoner Core API Data")
            for summoner in summoner_list:
                if summoner_name.lower() == summoner.name.lower():
                    print("Found Existing Summoner")
                    detail_view_url = "/summoner/?summoner_id={summoner_id}".format(
                        summoner_id=summoner.id
                    )
                    return HttpResponseRedirect(detail_view_url)
    
            new_name = summoner_name.lower().replace(" ", "")
            display_name = summoner_core_info[new_name]['name']
            riot_id = summoner_core_info[new_name]['id']
            level = summoner_core_info[new_name]['summonerLevel']
            newSummoner = Summoner(
                name=display_name,
                riot_id=riot_id,
                level=level
            )
            newSummoner.save()
            
            detail_view_url = "/summoner/?summoner_id={summoner_id}".format(
                summoner_id=newSummoner.id
            )    
            return HttpResponseRedirect(detail_view_url)
        else:
            error.summoner_not_exist = True
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")