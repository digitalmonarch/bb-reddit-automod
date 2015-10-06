#!/usr/bin/env python2.7
import shelve
import praw
import time
import logging
from prawoauth2 import PrawOAuth2Mini
import os

def load_games():
    #Open the DB and load of all the possible keys into a collection called 'keys'
    logging.info("Opening local database...")
    schedule = shelve.open(db_path)
    keys = schedule.keys()

    #For each key in the collection which has not yet been posted, load pertinant game data into memory
    logging.info("Loading future games into memory...")
    del remainingGames[:]
    for key in keys:
        entry = schedule[key]
        #What type of game is it?
        if entry['season_type'] == 'PRE':
            sType = 'Preseason '
        elif entry['season_type'] == 'POST':
            sType = 'Postseason '
        else:
            sType = ''
        info = {
            'key' : key,
            'preGameThreadTitle' : "Pre-Game Thread: " + entry['away'] + " @ " + entry['home'] + " - " + sType + "Week " + str(entry['week']) + ", " + str(entry['year']),
            't' : time.strptime(str(entry['year']) + " " + str(entry['month']) + " " + str(entry['day']) + " " + entry['time'],"%Y %m %d %I:%M %p"),
            'gameDayThreadTitle' : "Game Thread: " + entry['away'] + " @ " + entry['home'] + " - " + sType + "Week " + str(entry['week']) + ", " + str(entry['year']),
            't' : time.strptime(str(entry['year']) + " " + str(entry['month']) + " " + str(entry['day']) + " " + entry['time'],"%Y %m %d %I:%M %p"),    
            'postGameThreadTitle' : "Post-Game Thread: " + entry['away'] + " @ " + entry['home'] + " - " + sType + "Week " + str(entry['week']) + ", " + str(entry['year']),
            't' : time.strptime(str(entry['year']) + " " + str(entry['month']) + " " + str(entry['day']) + " " + entry['time'],"%Y %m %d %I:%M %p"),
            'preGamePosted' : entry['preGamePosted'],
            'gameDayPosted' : entry['gameDayPosted'],
            'postGamePosted' : entry['postGamePosted']
        }
        remainingGames.append(info)
    schedule.close()

#Reddit Authentication
def authenticate():
    global oauth_helper
    global reddit_client
    
    logging.info("Authenticating to Reddit...")
    reddit_client = praw.Reddit(user_agent=user_agent)
    oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)

#Check the current time against the list of remaining games. If a game will start soon, post the gameday thread
def game_thread_check():
    for game in remainingGames:
        global postedSomething
        
        #Post the pre-game thread on or after 8am on the day of the game
        if ((game['t'][0] == time.localtime()[0] and game['t'][1] == time.localtime()[1] and game['t'][2] == time.localtime()[2] and time.localtime()[3] >= 8) and (game['preGamePosted'] is False)):
            
            #Post the thread
            logging.info("A game is scheduled today. Posting pregame thread...")
            authenticate()
            oauth_helper.refresh()
            submission = reddit_client.submit(subreddit, game['preGameThreadTitle'], text="Go Bills!")
            url = submission.url.replace("reddit.com","reddit-stream.com",1)
            editedText = ("* Use [Reddit-Stream]("+ url + ") to follow comments on this post in real-time.\n\n"
            "* Go Bills!")
            submission.edit(editedText)
            
            #Update the database to indicate that this thread has been posted
            logging.info("Updating preGamePosted value for this game record...")
            schedule = shelve.open(db_path)
            entry = schedule[game['key']]
            entry['preGamePosted'] = True
            postedSomething = True
            schedule[game['key']] = entry
            schedule.close()
            
            #Sticky the thread
            logging.info("Stickying the thread")
            submission.sticky()
            logging.info("Update complete.")
        
        #If within the post threshold for game threads and the thread hasn't already been posted, post it.
        if ((time.mktime(game['t'])-gameDayPostThreshold <= time.time() <= time.mktime(game['t'])) and (game['gameDayPosted'] is False)):
            
            #Post the thread
            logging.info("A game is scheduled to start. Posting gameday thread...")
            authenticate()
            oauth_helper.refresh()
            submission = reddit_client.submit(subreddit, game['gameDayThreadTitle'], 
                text=("* Please be mindful of our sidebar rules.\n\n"
                "* Please report any violations.\n\n"
                "* Self-post threads are subject to deletion during and after the game.\n\n"
                "* Go Bills!"))
            url = submission.url.replace("reddit.com","reddit-stream.com",1)
            editedText = ("* Please be mindful of our sidebar rules.\n\n"
            "* Please report any violations.\n\n"
            "* Self-post threads are subject to deletion during and after the game.\n\n"
            "* Use [Reddit-Stream]("+ url + ") to follow comments on this post in real-time.\n\n"
            "* Join the conversation on [GroupMe](https://groupme.com/join_group/13046369/yUNI2l)\n\n"
            "* Find us on Twitter [@rbuffalobills](https://twitter.com/rBuffaloBills)\n\n"
            "* Go Bills!")
            submission.edit(editedText)
            
            #Update the database to indicate that this thread has been posted
            logging.info("Updating gameDayPosted value for this game record...")
            schedule = shelve.open(db_path)
            entry = schedule[game['key']]
            entry['gameDayPosted'] = True
            postedSomething = True
            schedule[game['key']] = entry
            schedule.close()

            #Sticky the thread
            logging.info("Stickying the thread")
            submission.sticky()

            #Begin monitoring the game
            logging.info("Starting game monitor")
            os.system("/usr/bin/python /home/pi/test/bb-game-monitor.py &")
            logging.info ("Update complete.")
            
try:
    #Load bot settings
    from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)
    
    #Configure logging
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)
    
    #Variable setup
    postedSomething = False
    remainingGames = []
    preGamePostThreshold = 18000 #Five hours (in seconds)
    gameDayPostThreshold = 3600 #One hour (in seconds)
       
    #Load unposted games into memory
    load_games()

    #Check for game threads
    logging.info("Checking for game threads...")
    game_thread_check()
    
    #If no threads were posted. Log a message and exit.
    if postedSomething is False:
        logging.info("No upcoming games found. Exiting.")
except:
    logging.exception("EXCEPTON OCCURRED")