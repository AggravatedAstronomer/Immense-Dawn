from __future__ import absolute_import
from mysite.celery import app

from StatTracker.RiotAPI import (
    RiotAPI, SubjectSummoner, IndexListScanner, ErrorHandler
)

@app.task(bind=True)
def celery_master_gather(self, summoner, summoner_id, psych_war_mod, threat_config):
    #self.update_state(state='PROGRESS')
    subject = SubjectSummoner(
        summoner.name,
        summoner_id,
        summoner.riot_id,
        summoner.level,
        psych_war_mod,
        threat_config
    )
    #self.update_state(state='DONE')
    return subject