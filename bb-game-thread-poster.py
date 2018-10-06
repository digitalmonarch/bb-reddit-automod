#!/usr/bin/env python2.7
import shelve
import praw
import time
import logging
import unicodedata
#from prawoauth2 import PrawOAuth2Mini
import os

def load_games():
    #Open the DB and load of all the possible keys into a collection called 'keys'
    logging.info("bb-game-thread-poster: Opening local database...")
    schedule = shelve.open(db_path)
    keys = schedule.keys()

    #For each key in the collection which has not yet been posted, load pertinant game data into memory
    logging.info("bb-game-thread-poster: Loading future games into memory...")
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
    #global oauth_helper
    global reddit_client
    
    logging.info("bb-game-thread-poster: Authenticating to Reddit...")
    reddit_client = praw.Reddit(user_agent=user_agent, client_id=app_key, client_secret=app_secret, refresh_token=refresh_token)
    #oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)

def pre_game_thread_check():
    for game in remainingGames:
        global postedSomething

        #Post the pre-game thread on or after 8am on the day of the game
        if ((game['t'][0] == time.localtime()[0] and game['t'][1] == time.localtime()[1] and game['t'][2] == time.localtime()[2] and time.localtime()[3] >= 8) and (game['preGamePosted'] is False)):
            logging.info("bb-game-thread-poster: A game is scheduled today. Posting pregame thread...")
            authenticate()
            submission = reddit_client.subreddit(subreddit).submit(game['preGameThreadTitle'], selftext="Go Bills!")
            #submission = reddit_client.submit(subreddit, game['preGameThreadTitle'], text="Go Bills!")
            url = submission.url.replace("reddit.com","reddit-stream.com",1)
            editedText = ("* Use [Reddit-Stream]("+ url + ") to follow comments on this post in real-time.\n\n"
            "* Go Bills!")
            submission.edit(editedText)
            
            #Update the database to indicate that this thread has been posted
            logging.info("bb-game-thread-poster: Updating preGamePosted value for this game record...")
            schedule = shelve.open(db_path)
            entry = schedule[game['key']]
            entry['preGamePosted'] = True
            postedSomething = True
            schedule[game['key']] = entry
            schedule.close()
            
            #Sticky the thread
            logging.info("bb-game-thread-poster: Stickying the thread")
            submission.mod.sticky(state=True)
            
            logging.info("bb-game-thread-poster: Pre-game thread logic complete....")

def game_thread_check():
    for game in remainingGames:
        global postedSomething
        
        #Post the game-thread if within the post threshold.
        if ((time.mktime(game['t'])-gameDayPostThreshold <= time.time() <= time.mktime(game['t'])) and (game['gameDayPosted'] is False)):
            logging.info("bb-game-thread-poster: A game is scheduled to start... Checking for pre-game thread to unsticky...")
            
            authenticate()

            #Check for a pre-game thread and unsticky it if found.
            for submission in reddit_client.subreddit(subreddit).hot(limit=2):
                if("Pre-Game Thread:" in submission.title):
                    logging.info("bb-game-thread-poster: Pre-game thread found... Attempting to unsticky it...")
                    submission.mod.sticky(state=False);

            #Post the gameday thread
            logging.info("bb-game-thread-poster: Posting gameday thread...")
            #submission = reddit_client.submit(subreddit, game['gameDayThreadTitle'], 
            submission = reddit_client.subreddit(subreddit).submit(game['gameDayThreadTitle'], 
                selftext=("* Please be mindful of our sidebar rules.\n\n"
                "* Please report any violations.\n\n"
                "* Self-post threads are subject to deletion during and after the game.\n\n"
                "* Go Bills!"))
            url = submission.url.replace("reddit.com","reddit-stream.com",1)
            editedText = ("* Please be mindful of our sidebar rules.\n\n"
            "* Please report any violations.\n\n"
            "* Self-post threads are subject to deletion during and after the game.\n\n"
            "* Use [Reddit-Stream]("+ url + ") to follow comments on this post in real-time.\n\n"
            "* Find us on Twitter [@rbuffalobills](https://twitter.com/rBuffaloBills)\n\n"
            "* Self-posts will be removed so that discussion is contained within our official gameday threads. This helps to prevent topic duplciation and fragmentation of the conversation.\n\n"
            "* Go Bills!")
            submission.edit(editedText)
            
            #Update the database to indicate that this thread has been posted
            logging.info("bb-game-thread-poster: Updating gameDayPosted value for this game record...")
            schedule = shelve.open(db_path)
            entry = schedule[game['key']]
            entry['gameDayPosted'] = True
            postedSomething = True
            schedule[game['key']] = entry
            schedule.close()

            #Sticky the thread
            logging.info("bb-game-thread-poster: Stickying the thread")
            submission.mod.sticky(state=True)

            #Set suggested sort to New
            logging.info("bb-game-thread-poster: Setting suggested sort")
            submission.mod.suggested_sort = 'new'

            #Add a comment to the thread
            logging.info("bb-game-thread-poster: Waiting 5 seconds...")
            time.sleep(5)
            logging.info("bb-game-thread-poster: Commenting on thread...")
            reddit_client.subreddit(subreddit).mod.distinguish(submission.reply("**Notice:** In an effort to ensure that /r/buffalobills remains a pleasant place to discuss the game, the moderation team will use reasonable discretion to remove comments which do not add to the conversation or are excessively negative."), how='yes')

            #Disable self-posts for the duration of the game
            logging.info("bb-game-thread-poster: Disabling self-posts until 30 minutes after the completion of the game...")
            reddit_client.subreddit(subreddit).mod.update(link_type="link")

            #Begin monitoring the game
            logging.info("bb-game-thread-poster: Starting game monitor")
            
            error=True
            
            while error:
                try:
                    os.system(python_path + " " + monitor_path + " &")
                    error=False
                except:
                    logging.exception("bb-tame-thread-poster: bb-game-monitor.py has crashed. Restarting.")
                    error=True

            logging.info ("Update complete")

def post_game_thread_check():
    #Remove post-game threads between 6am and 7am EST only.
    if(time.localtime()[3] == 06):
        authenticate()
        for submission in reddit_client.subreddit(subreddit).hot(limit=2):
            if("Post-Game Thread:" in submission.title):
                logging.info("bb-game-thread-poster: Post-game thread found... Attempting to unsticky it...")
                submission.mod.sticky(state=False);
            
try:
    #Load bot settings
    from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path, python_path, monitor_path)
    
    #Configure logging
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)
    
    #Variable setup
    postedSomething = False
    remainingGames = []
    gameDayPostThreshold = 900 #15 minutes (in seconds)
       
    #Load unposted games into memory
    load_games()

    #Check for pre-game threads
    logging.info("bb-game-thread-poster: Checking for pre-game threads...")
    pre_game_thread_check()

    #Check for game threads
    logging.info("bb-game-thread-poster: Checking for game threads...")
    game_thread_check()
    
    #Check for post-game threads after 6am and unsticky them.
    logging.info("bb-game-thread-poster: Checking for post-game threads...")
    post_game_thread_check()

    #If no threads were posted. Log a message and exit.
    if postedSomething is False:
        logging.info("bb-game-thread-poster: Nothing to do. Exiting.")
        
except:
    logging.exception("bb-game-thread-poster: EXCEPTION OCCURRED")