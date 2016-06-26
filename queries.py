#!/usr/bin/env python2.7
import nflgame.game
import logging

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

games = nflgame.games(2015, week=[16])
for g in games:
    if (g.home == 'BUF' or g.away == 'BUF'):
        #Add below code to bb-game-monitor.py

        #Put this at launch. No need to call it every time.
        for t in nflgame.teams:
            if t[0] == g.home:
                home_friendlyName = t[3]
            elif t[0] == g.away:
                away_friendlyName = t[3]

        editedText = ("***\n"
            "||Score\n"
            "---|:-:\n" + 
            "[](/" + g.home +") **" + home_friendlyName + "**|" + str(g.score_home) + "\n"
            "[](/" + g.away +") **" + away_friendlyName + "**|" + str(g.score_away) + "\n"
            "***\n**Team Statistics:**\n\n"
            "||[](/"+ g.home +")|[](/"+ g.away +")|\n"
            "|:--|:--:|:--:|\n"
            "|First Downs|" + str(g.stats_home[0]) + "|" + str(g.stats_away[0]) + "|\n"
            "|Total Yards|" + str(g.stats_home[1]) + "|" + str(g.stats_away[1]) + "|\n"
            "|Passing Yards|" + str(g.stats_home[2]) + "|" + str(g.stats_away[2]) + "|\n"
            "|Rushing Yards|" + str(g.stats_home[3]) + "|" + str(g.stats_away[3]) + "|\n"
            "|Penalties|" + str(g.stats_home[4]) + "|" + str(g.stats_away[4]) + "|\n"
            "|Penalty Yards|" + str(g.stats_home[5]) + "|" + str(g.stats_away[5]) + "|\n"
            "|Turnovers|" + str(g.stats_home[6]) + "|" + str(g.stats_away[6]) + "|\n"
            "|Punts|" + str(g.stats_home[7]) + "|" + str(g.stats_away[7]) + "|\n"
            "|Time of Possession|" + str(g.stats_home[10]) + "|" + str(g.stats_away[10]) + "|\n"
            "***\n**Top Performers:**\n"
            "***\n**Scoring Summary:**\n"
            "***\n**Around the League:**\n"
            )

        print editedText
       
        # print "{0} Won Over {1} - {2} - {3} Week {4}".format(g.winner, g.loser, g.score_home, g.score_away, g.schedule['week'])

        # print g.score_home
        # print g.score_away
     
        # print "\nTeam Stats"
        # print 'Home Team: ', g.stats_home
        # print 'Away Team: ', g.stats_away

        # #Build arrays containing the leading passers of each team
        # homePassing = []
        # awayPassing = []

        # for p in g.players.passing().filter(team = g.home).sort("passing_yds"):
        #     homePassing.append(p)

        # for p in g.players.passing().filter(team = g.away).sort("passing_yds"):
        #     awayPassing.append(p)

        # print "\nPassing Leaders"
        # print homePassing[0].team, homePassing[0], homePassing[0].passing_cmp, homePassing[0].passing_att, homePassing[0].passing_yds, homePassing[0].passing_tds, homePassing[0].passing_int
        # print awayPassing[0].team, awayPassing[0], awayPassing[0].passing_cmp, awayPassing[0].passing_att, awayPassing[0].passing_yds, awayPassing[0].passing_tds, awayPassing[0].passing_int

        # #Build arrays containing the leading rushers of each team
        # homeRushing = []
        # awayRushing = []

        # for p in g.players.rushing().filter(team = g.home).sort("rushing_yds"):
        #     homeRushing.append(p)

        # for p in g.players.rushing().filter(team = g.away).sort("rushing_yds"):
        #     awayRushing.append(p)

        # print "\nRushing Leaders"
        # print homeRushing[0].team, homeRushing[0], homeRushing[0].rushing_att, homeRushing[0].rushing_yds, homeRushing[0].rushing_tds
        # print awayRushing[0].team, awayRushing[0], awayRushing[0].rushing_att, awayRushing[0].rushing_yds, awayRushing[0].rushing_tds

        # #Build arrays containing the leading receivers of each team
        # homeReceiving = []
        # awayReceiving = []

        # for p in g.players.receiving().filter(team = g.home).sort("receiving_yds"):
        #     homeReceiving.append(p)

        # for p in g.players.receiving().filter(team = g.away).sort("receiving_yds"):
        #     awayReceiving.append(p)

        # print "\nReceiving Leaders"
        # print homeReceiving[0].team, homeReceiving[0], homeReceiving[0].receiving_rec, homeReceiving[0].receiving_yds, homeReceiving[0].receiving_tds
        # print awayReceiving[0].team, awayReceiving[0], awayReceiving[0].receiving_rec, awayReceiving[0].receiving_yds, awayReceiving[0].receiving_tds

        # print "\nScoring Summary"
        # print g.scores

        # print "\nSchedule"
        # print g.schedule

        #Add above code to bb-game-monitor.py