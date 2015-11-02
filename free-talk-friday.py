#!/usr/bin/env python2.7
import praw
import time
import logging
from prawoauth2 import PrawOAuth2Mini

#Reddit Authentication
def authenticate():
    global oauth_helper
    global reddit_client
    
    logging.info("Authenticating to Reddit...")
    reddit_client = praw.Reddit(user_agent=user_agent)
    oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)
            
try:
    #Load bot settings
    from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path, monitor_path)
    
    #Configure logging
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)
    
    if (time.strftime('%a', time.localtime()) == "Fri"):
        logging.info("Time to post free-talk Friday thread.")

        #Authenticate
        authenticate()
        oauth_helper.refresh()

        #Post Thread
        threadTitle = "Feedback, Fantasy, and Free-Talk Friday - " + time.strftime('%m/%d/%Y', time.localtime())
        threadBody = (
        "**Feedback** - Got a suggestion about what you'd like to see out of the sub? This is the place to put it; just reply to /u/BillsMod's comment for whatever you might like to say.\n\n"
        "**Fantasy Talk** - Since fantasy threads are something we discourage across the sub, this is a place to go for some Bills-specific questions or thoughts. **/r/fantasyfootball** is still the place one should go for the best insight and higher quality or pointed discussion, but here's an in-house solution to bring up something minor.\n\n"
        "**Free Talk** - Self-explanatory. Here if you just feel like riffing, man. How about those new red uniforms though?\n\n"
        "As always, please adhere to our rules.  Happy Friday!"
        )

        logging.info("Posting thread...")
        submission = reddit_client.submit(subreddit, threadTitle, threadBody)

        logging.info("Stickying thread...")
        submission.sticky()
        
        time.sleep(10)
        logging.info("Commenting on thread...")
        submission.add_comment("**Please reply to this comment with any feedback, ideas, or suggestions you may have for the mod team about the subreddit.**")

        logging.info("All done. Exiting...")

    elif (time.strftime('%a', time.localtime()) == "Sat"):

        #Authenticate
        authenticate()
        oauth_helper.refresh()

        #Check top two posts and unsticky any free-talk friday threads.
        logging.info("Begin search for free-talk friday threads to unsticky.")
        
        for submission in reddit_client.get_subreddit(subreddit).get_hot(limit=2):
            if("Feedback, Fantasy, and Free-Talk Friday" in str(submission)):
                logging.info("Free-talk Friday thread found. Attempting to unsticky it.")
                submission.unsticky();

except:
    logging.exception("EXCEPTON OCCURRED")