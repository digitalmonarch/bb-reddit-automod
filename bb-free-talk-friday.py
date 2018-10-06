#!/usr/bin/env python2.7
import praw
import time
import logging
import unicodedata
#from prawoauth2 import PrawOAuth2Mini

#Reddit Authentication
def authenticate():
    #global oauth_helper
    global reddit_client
    
    logging.info("bb-free-talk-friday: Authenticating to Reddit...")
    reddit_client = praw.Reddit(user_agent=user_agent, client_id=app_key, client_secret=app_secret, refresh_token=refresh_token)
    #oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)
            
try:
    #Load bot settings
    from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path, monitor_path)
    
    #Configure logging
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)
    
    logging.info("bb-free-talk-friday: Free-talk Friday - Beginning day of week check.")

    if (time.strftime('%a', time.localtime()) == "Fri"):
        logging.info("bb-free-talk-friday: Post free-talk Friday thread.")

        #Authenticate
        authenticate()

        #Post Thread
        threadTitle = "Free-Talk Friday - " + time.strftime('%m/%d/%Y', time.localtime())
        threadBody = (
        "**Feedback** - Got a suggestion for the mods? This is the place to put it. Just reply to /u/BillsMod's comment below.\n\n"
        "**Fantasy Football** - **/r/fantasyfootball** is still the place one should go for the best insight and higher quality or pointed discussion, but feel free to chat here if you wish.\n\n"
        "**Free Talk** - Self-explanatory.\n\n"
        "As always, please adhere to our rules.  Happy Friday!"
        )

        logging.info("bb-free-talk-friday: Posting thread...")
        submission = reddit_client.subreddit(subreddit).submit(threadTitle, threadBody)
        #submission = reddit_client.submit(subreddit, threadTitle, threadBody)

        logging.info("bb-free-talk-friday: Stickying thread...")
        submission.mod.sticky(state=True)
        
        time.sleep(10)
        logging.info("bb-free-talk-friday: Commenting on thread...")
        reddit_client.subreddit(subreddit).mod.distinguish(submission.reply("**Got a suggestion for the mods? Reply here and let us know.**"), how='yes')

        logging.info("bb-free-talk-friday: All done. Exiting...")

    elif (time.strftime('%a', time.localtime()) == "Sat"):

        #Authenticate
        authenticate()

        #Check top two posts and unsticky any free-talk friday threads.
        logging.info("bb-free-talk-friday: Begin search for free-talk friday threads to unsticky.")
        
        for submission in reddit_client.subreddit(subreddit).hot(limit=2):
            if("Free-Talk Friday" in submission.title):
                logging.info("bb-free-talk-friday: Free-talk Friday thread found. Removing sticky.")
                submission.mod.sticky(state=False)

except:
    logging.exception("EXCEPTION OCCURRED")