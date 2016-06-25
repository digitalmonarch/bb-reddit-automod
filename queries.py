#!/usr/bin/env python2.7
import nflgame.game
import logging

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

games = nflgame.games(2015, week=[17])
for g in games:
    if (g.home == 'BUF' or g.away == 'BUF'):
        #Add below code to bb-game-monitor.py
       
        print "{0} Won Over {1} - Week {2}".format(g.winner, g.loser, g.schedule['week'])

        #Build arrays containing the leading passers of each team
        homePassing = []
        awayPassing = []

        for p in g.players.passing().filter(team = g.home).sort("passing_yds"):
            homePassing.append(p)

        for p in g.players.passing().filter(team = g.away).sort("passing_yds"):
            awayPassing.append(p)

        print "\nPassing Leaders"
        print homePassing[0].team, homePassing[0], homePassing[0].passing_cmp, homePassing[0].passing_att, homePassing[0].passing_yds, homePassing[0].passing_tds, homePassing[0].passing_int
        print awayPassing[0].team, awayPassing[0], awayPassing[0].passing_cmp, awayPassing[0].passing_att, awayPassing[0].passing_yds, awayPassing[0].passing_tds, awayPassing[0].passing_int

        #Build arrays containing the leading rushers of each team
        homeRushing = []
        awayRushing = []

        for p in g.players.rushing().filter(team = g.home).sort("rushing_yds"):
            homeRushing.append(p)

        for p in g.players.rushing().filter(team = g.away).sort("rushing_yds"):
            awayRushing.append(p)

        print "\nRushing Leaders"
        print homeRushing[0].team, homeRushing[0], homeRushing[0].rushing_att, homeRushing[0].rushing_yds, homeRushing[0].rushing_tds
        print awayRushing[0].team, awayRushing[0], awayRushing[0].rushing_att, awayRushing[0].rushing_yds, awayRushing[0].rushing_tds

        #Build arrays containing the leading receivers of each team
        homeReceiving = []
        awayReceiving = []

        for p in g.players.receiving().filter(team = g.home).sort("receiving_yds"):
            homeReceiving.append(p)

        for p in g.players.receiving().filter(team = g.away).sort("receiving_yds"):
            awayReceiving.append(p)

        print "\nReceiving Leaders"
        print homeReceiving[0].team, homeReceiving[0], homeReceiving[0].receiving_rec, homeReceiving[0].receiving_yds, homeReceiving[0].receiving_tds
        print awayReceiving[0].team, awayReceiving[0], awayReceiving[0].receiving_rec, awayReceiving[0].receiving_yds, awayReceiving[0].receiving_tds

        #Add above code to bb-game-monitor.py