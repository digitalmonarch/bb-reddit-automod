#!/usr/bin/env python2.7
import nflgame.live
import nflgame.game
import logging
import praw
import os
import time
from prawoauth2 import PrawOAuth2Mini

#Reddit Authentication
def authenticate():
    global oauth_helper
    global reddit_client
    
    logging.info("bb-game-monitor: Authenticating to Reddit...")
    reddit_client = praw.Reddit(user_agent=user_agent)
    oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)

def getSubmission():
    global gameThreadSubmission
    gameThreadSubmission = None
    for submission in reddit_client.get_subreddit(subreddit).get_hot(limit=1):
        if("Game Thread:" in str(submission) and "Pre-Game" not in str(submission)):
            logging.info("bb-game-monitor: Game thread found. Storing submission object...")
            gameThreadSubmission = submission

#Callback function
def cb(active, completed, diffs):
    for g in active:
        if (g.home == 'BUF' or g.away == 'BUF'):
            
            #Log this visit
            time_remaining = str(g.time)
            gameInfo = 'bb-game-monitor: %s :: %s (%d) vs. %s (%d)' % (time_remaining, g.home, g.score_home, g.away, g.score_away)
            logging.info(gameInfo)

            #Define the friendly names of both teams
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

            editedText = ("***\n**Scoreboard:**\n\n"
                "***\n"
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
                )
            if(homePassing and awayPassing):
                editedText+=(
                    "| **Passing** | **Name**  | **Cmp/Att** | **Yds** | **TDs** | **Ints** |\n"
                    "|[](/" + g.home + ")|" + str(homePassing[0]) + "|" + str(homePassing[0].passing_cmp) + "/" + str(homePassing[0].passing_att) + "|" + str(homePassing[0].passing_yds) + "|" + str(homePassing[0].passing_tds) + "|" + str(homePassing[0].passing_int) + "|\n"
                    "|[](/" + g.away + ")|" + str(awayPassing[0]) + "|" + str(awayPassing[0].passing_cmp) + "/" + str(awayPassing[0].passing_att) + "|" + str(awayPassing[0].passing_yds) + "|" + str(awayPassing[0].passing_tds) + "|" + str(awayPassing[0].passing_int) + "|\n"
                    )
            if(homeRushing and awayRushing):
                editedText+=(
                    "| **Rushing** | **Name**  | **Car** | **Yds** | **TDs** | **Fum** |\n"
                    "|[](/" + g.home + ")|" + str(homeRushing[0]) + "|" + str(homeRushing[0].rushing_att) + "|" + str(homeRushing[0].rushing_yds) + "|" + str(homeRushing[0].rushing_tds) + "|" + str(homeRushing[0].fumbles_lost) + "|\n"
                    "|[](/" + g.away + ")|" + str(awayRushing[0]) + "|" + str(awayRushing[0].rushing_att) + "|" + str(awayRushing[0].rushing_yds) + "|" + str(awayRushing[0].rushing_tds) + "|" + str(awayRushing[0].fumbles_lost) + "|\n"
                    )
            if(homeReceiving and awayReceiving):
                editedText+=(
                    "| **Receiving** | **Name**  | **Rec** | **Yds** | **TDs** | **Fum** |\n"
                    "|[](/" + g.home + ")|" + str(homeReceiving[0]) + "|" + str(homeReceiving[0].receiving_rec) + "|" + str(homeReceiving[0].receiving_yds) + "|" + str(homeReceiving[0].receiving_tds) + "|" + str(homeReceiving[0].fumbles_lost) + "|\n"
                    "|[](/" + g.away + ")|" + str(awayReceiving[0]) + "|" + str(awayReceiving[0].receiving_rec) + "|" + str(awayReceiving[0].receiving_yds) + "|" + str(awayReceiving[0].receiving_tds) + "|" + str(awayReceiving[0].fumbles_lost) + "|\n"
                    )
            editedText+=(
                "***\n**Scoring Summary:**\n\n"
                "| **Qtr** | **Team** |**Type** | **Description**|\n"
                "| :--: | :--: | :--: | :-- |\n"
                )

            #Build a string representing the scoring summary and concat it to editedText
            scoringSummaryText = ""

            for s in g.scores:
                scoringSummaryText += "|" + s.split(' - ')[1] + "|[](/" + s.split(' - ')[0] + ")|" + s.split(' - ')[2] + "|" + s.split(' - ')[3] + "|\n"

            editedText += scoringSummaryText
            
            #Don't post the Around the League scoreboxes during the last edit since the scores will stop updating after the game is over.
            if(str(g.time).upper() != "Q4 00:00"):
                editedText += ("***\n**Around the League:**\n\n"
                    "Home |Away  |Clock  |\n"
                    "---|---|----\n"
                    )

                #Build a string representing scores from around the league and concat it to editedText
                AroundTheLeagueText = ""

                for g in active:
                    #print g.home, g.score_home, g.away, g.score_away, g.time
                    AroundTheLeagueText += "[](/" + g.home + ") "+ str(g.score_home) + "| [](/" + g.away + ") " + str(g.score_away) + "| " + str(g.time).upper() + "|\n"
                        
                editedText += AroundTheLeagueText

            #Authenticate to reddit and update the gameday thread
            logging.info("bb-game-monitor: Updating game thread body...")
            #authenticate()
            oauth_helper.refresh()
            gameThreadSubmission.edit(editedText)

    #Check to see whether or not to post the post game thread.
    #Previously did this at the 2 minute warning. time_remaining == 'Q4 02:00' or time_remaining.startswith('Q4 01')):
    logging.info("bb-game-monitor: Checking whether or not to post the post-game thread...")
    for g in completed:
        if (g.home == 'BUF' or g.away == 'BUF'):

            #Log this visit
            time_remaining = str(g.time)
            gameInfo = '%s :: %s (%d) vs. %s (%d)' % (time_remaining, g.home, g.score_home, g.away, g.score_away)
            logging.info(gameInfo)

            logging.info("bb-game-monitor: Game has ended. Find the game thread and unsticky it.")

            #Define the friendly names of both teams
            for t in nflgame.teams:
                if t[0] == g.home:
                    home_friendlyName = t[3]
                elif t[0] == g.away:
                    away_friendlyName = t[3]

            #authenticate()
            oauth_helper.refresh()

            #Check for a game thread and unsticky it if found.
            for submission in reddit_client.get_subreddit(subreddit).get_hot(limit=2):
                if("Game Thread:" in str(submission) and "Pre-Game" not in str(submission)):
                    logging.info("bb-game-monitor: Game thread found... Attempting to unsticky it...")
                    submission.unsticky();

            #Post the post-game thread
            postGameThreadTitle = "Post-Game Thread: " + g.away + " @ " + g.home + " (Week " + str(g.schedule['week']) + ")"
            postGameThreadText = ""

            if (g.winner == 'BUF'):
                logging.info("bb-game-monitor: Bills win!!!")
                postGameThreadText = ("[BILLS WIN!](https://www.youtube.com/watch?v=PHbnQXsyDrE)\n\n"
                    "* Please be mindful of our sidebar rules.\n"
                    "* Please report any violations.\n"
                    "* Self-posts will be removed so that discussion is contained within our official gameday threads. This helps to prevent topic duplciation and fragmentation of the conversation.\n"
                    "\n**Scoreboard:**\n\n"
                    "***\n"
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
                    "|Time of Possession|" + str(g.stats_home[10]) + "|" + str(g.stats_away[10]) + "|\n")
            else:
                logging.info("bb-game-monitor: Bills lose...")
                postGameThreadText = ("[Bills Lose... :(](https://www.youtube.com/watch?v=yJxCdh1Ps48)\n\n"
                    "* Please be mindful of our sidebar rules.\n"
                    "* Please report any violations.\n"
                    "* Self-posts will be removed so that discussion is contained within our official gameday threads. This helps to prevent topic duplciation and fragmentation of the conversation.\n"
                    "\n**Scoreboard:**\n\n"
                    "***\n"
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
                    "|Time of Possession|" + str(g.stats_home[10]) + "|" + str(g.stats_away[10]) + "|\n" )

            logging.info("bb-game-monitor: Posting post game thread...")
            submission = reddit_client.submit(subreddit, postGameThreadTitle, postGameThreadText)

            #Sticky the thread
            logging.info("bb-game-monitor: Stickying the thread...")
            submission.sticky()
            logging.info("bb-game-monitor: Update complete. Exiting game monitor...")

            os._exit(1)

try:
    #Load bot settings
    from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

    #Configure logging
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

    logging.info("bb-game-monitor: Starting bb-game-monitor...")

    #Get the game thread submission object and store it in a global variable.
    logging.info("bb-game-monitor: Begin search for game thread submission object...")
    
    authenticate()
    
    #Initialize gameThreadSubmission to None so that we can re-try the search if necessary.
    getSubmission()

    while (gameThreadSubmission is None):
        logging.info("bb-game-monitor: Game thread not found. Will try again in 30 seconds...")
        time.sleep(30)
        getSubmission()

    #Begin monitoring the game.
    logging.info("bb-game-monitor: Beginning monitoring...")
    nflgame.live.run(cb, active_interval=30)

except:
    logging.exception("bb-game-monitor: EXCEPTON OCCURRED")