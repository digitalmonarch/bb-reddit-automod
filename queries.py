#!/usr/bin/env python2.7
import nflgame.game
import logging

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

games = nflgame.games(2017, week=[2])
for g in games:
    print g.home
    print g.away

print "------------------------------------"

for t in nflgame.teams:
   print t[0]

    # if (g.home == 'BUF' or g.away == 'BUF'):
    #     #Add below code to bb-game-monitor.py

    #     #Put this at launch. No need to call it every time.
    #     for t in nflgame.teams:
    #         if t[0] == g.home:
    #             home_friendlyName = t[3]
    #         elif t[0] == g.away:
    #             away_friendlyName = t[3]

        