# PsychologicalWarfare
A simple stat tracking tool for League of Legends to predict the outcome of Ranked 5v5 games.

It projects player psychology based on match history. This is achieved by modelling the player's state of mind based on their most recent consecutive results (winning and losing streaks), and their
win-loss-ratio over the past x games, where x a configurable integer. Players are assigned a state of mind, and a corresponding severity coefficient to model the extent to which that mentality is
likely to be exhibited. (State: Confident or Vulnerable, Severity: Minimal, Low, Moderate, High, Extreme)

It also bases its predictions on the win-loss-ratio of the player with the champion whom they are currently playing as in the subject match.

In addition to predicting the outcome of Ranked 5v5 games, it returns a compact, visually-appealing overview of the subject summoner (the player being looked up) with an emphasis on readability and
instant access to the most pertinent information.

The application also has a self-diagnostic system. For a game to result in a prediction being made, it must be a 5v5 Ranked game where there is a projected overall advantage favouring one team to win by a minimum value. (ie, Team 1 has a 52% chance to win, by extension Team 2 has a 48% chance). 5v5 Ranked games that are too closely matched will return an inconclusive result.

Where a game results in a prediction, a diagnostic caretaker object will be created to store the match's unique ID, the prediction made about who will win, and the certainty with which that prediction
is made. Each time the index page is loaded, the server iterates through the caretaker objects stored in the database, making an API request for data regarding the game with its stored ID. If the game is not yet finished, it will wait until next time. If it has finished, it will recieve .json output describing that game, find out who won, pass its information to the central 'Overseer' database object, and delete itself from the database.

The Overseer database object is updated to reflect the new data regarding successful and failed predictions, and return a success rate displayed in the Index. It is harder to successfully predict higher level games, as the games tend to be closer, and the players tend to be less prone to psychological influences (tilt, rage, etc).

# Installation
* git clone git@github.com:AggravatedAstronomer/PsychologicalWarfare.git
* cd PsychologicalWarfare
* virtualenv .
* . bin/activate
* pip install -r requirements.txt
* ./manage.py migrate
* ./manage.py runserver

Add RIOT_API_KEY to mysite/local_settings.py
