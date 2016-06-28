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

        #Build six arrays containing the statistics of the leading passers, rushers and receivers on each team.
        homePassing, awayPassing, homeRushing, awayRushing, homeReceiving, awayReceiving = ([] for i in range(6))

        for p in g.players.passing().filter(team = g.home).sort("passing_yds"):
            homePassing.append(p)

        for p in g.players.passing().filter(team = g.away).sort("passing_yds"):
            awayPassing.append(p)
        
        for p in g.players.rushing().filter(team = g.home).sort("rushing_yds"):
            homeRushing.append(p)

        for p in g.players.rushing().filter(team = g.away).sort("rushing_yds"):
            awayRushing.append(p)
        
        for p in g.players.receiving().filter(team = g.home).sort("receiving_yds"):
            homeReceiving.append(p)

        for p in g.players.receiving().filter(team = g.away).sort("receiving_yds"):
            awayReceiving.append(p)

        editedText = ("***\n"
            "| | |\n"
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
            "***\n**Top Performers:**\n\n"
            "| | | | | | |\n"
            "| :--: | :-- | :--: | :--: | :--: | :--: |\n"
            "| **Passing** | **Name**  | **Cmp/Att** | **Yds** | **TDs** | **Ints** |\n"
            "|[](/" + g.home + ")|" + str(homePassing[0]) + "|" + str(homePassing[0].passing_cmp) + "/" + str(homePassing[0].passing_att) + "|" + str(homePassing[0].passing_yds) + "|" + str(homePassing[0].passing_tds) + "|" + str(homePassing[0].passing_int) + "|\n"
            "|[](/" + g.away + ")|" + str(awayPassing[0]) + "|" + str(awayPassing[0].passing_cmp) + "/" + str(awayPassing[0].passing_att) + "|" + str(awayPassing[0].passing_yds) + "|" + str(awayPassing[0].passing_tds) + "|" + str(awayPassing[0].passing_int) + "|\n"
            "| **Rushing** | **Name**  | **Car** | **Yds** | **TDs** | **Fum** |\n"
            "|[](/" + g.home + ")|" + str(homeRushing[0]) + "|" + str(homeRushing[0].rushing_att) + "|" + str(homeRushing[0].rushing_yds) + "|" + str(homeRushing[0].rushing_tds) + "|" + str(homeRushing[0].fumbles_lost) + "|\n"
            "|[](/" + g.away + ")|" + str(awayRushing[0]) + "|" + str(awayRushing[0].rushing_att) + "|" + str(awayRushing[0].rushing_yds) + "|" + str(awayRushing[0].rushing_tds) + "|" + str(awayRushing[0].fumbles_lost) + "|\n"
            "| **Receiving** | **Name**  | **Rec** | **Yds** | **TDs** | **Fum** |\n"
            "|[](/" + g.home + ")|" + str(homeReceiving[0]) + "|" + str(homeReceiving[0].receiving_rec) + "|" + str(homeReceiving[0].receiving_yds) + "|" + str(homeReceiving[0].receiving_tds) + "|" + str(homeReceiving[0].fumbles_lost) + "|\n"
            "|[](/" + g.away + ")|" + str(awayReceiving[0]) + "|" + str(awayReceiving[0].receiving_rec) + "|" + str(awayReceiving[0].receiving_yds) + "|" + str(awayReceiving[0].receiving_tds) + "|" + str(awayReceiving[0].fumbles_lost) + "|\n"
            "***\n**Scoring Summary:**\n\n"
            "| **Qtr** | **Team** |**Type** | **Description**|\n"
            "| :--: | :--: | :--: | :-- |\n"
            )

        #Build a string representing the scoring summary and concat it to editedText
        scoringSummaryText = ""

        for s in g.scores:
            scoringSummaryText += "|" + s.split(' - ')[1] + "|[](/" + s.split(' - ')[0] + ")|" + s.split(' - ')[2] + "|" + s.split(' - ')[3] + "|\n"

        editedText += scoringSummaryText
        editedText += ("***\n**Around the League:**\n\n"
            "| | | | | | | | |\n"
            "| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |\n"
            )

        #Build a string representing scores from around the league and concat it to editedText
        AroundTheLeagueText = ""

        for g in games:
            AroundTheLeagueText += str(g)
            
        editedText += AroundTheLeagueText

        print editedText

        #Add above code to bb-game-monitor.py

        # print "{0} Won Over {1} - {2} - {3} Week {4}".format(g.winner, g.loser, g.score_home, g.score_away, g.schedule['week'])