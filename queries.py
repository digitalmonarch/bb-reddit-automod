#!/usr/bin/env python2.7
import nflgame.game
import logging

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)


for g in nflgame.games(2015, week=13):
    if (g.home == 'BUF' or g.away == 'BUF'):
        home = g.home
        away = g.away

game = nflgame.one(2015, 13, home, away)

#Build arrays containing the leading passers of each team
homePassing = []
awayPassing = []

for p in game.players.passing().filter(team = home).sort("passing_yds"):
    homePassing.append(p)

for p in game.players.passing().filter(team = away).sort("passing_yds"):
    awayPassing.append(p)

print "Passing Leaders"
print homePassing[0].team, homePassing[0], homePassing[0].passing_cmp, homePassing[0].passing_att, homePassing[0].passing_yds, homePassing[0].passing_tds, homePassing[0].passing_int
print awayPassing[0].team, awayPassing[0], awayPassing[0].passing_cmp, awayPassing[0].passing_att, awayPassing[0].passing_yds, awayPassing[0].passing_tds, awayPassing[0].passing_int

#Build arrays containing the leading rushers of each team
homeRushing = []
awayRushing = []

for p in game.players.rushing().filter(team = home).sort("rushing_yds"):
    homeRushing.append(p)

for p in game.players.rushing().filter(team = away).sort("rushing_yds"):
    awayRushing.append(p)

print "\nRushing Leaders"
print homeRushing[0].team, homeRushing[0], homeRushing[0].rushing_att, homeRushing[0].rushing_yds, homeRushing[0].rushing_tds
print awayRushing[0].team, awayRushing[0], awayRushing[0].rushing_att, awayRushing[0].rushing_yds, awayRushing[0].rushing_tds

#Build arrays containing the leading receivers of each team
homeReceiving = []
awayReceiving = []

for p in game.players.receiving().filter(team = home).sort("receiving_yds"):
    homeReceiving.append(p)

for p in game.players.receiving().filter(team = away).sort("receiving_yds"):
    awayReceiving.append(p)

print "\nReceiving Leaders"
print homeReceiving[0].team, homeReceiving[0], homeReceiving[0].receiving_rec, homeReceiving[0].receiving_yds, homeReceiving[0].receiving_tds
print awayReceiving[0].team, awayReceiving[0], awayReceiving[0].receiving_rec, awayReceiving[0].receiving_yds, awayReceiving[0].receiving_tds
