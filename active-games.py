#!/usr/bin/env python2.7
import nflgame.live
import logging

#Load bot settings
from settings import (log_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

#Get the current week and year and build a list of all active games
year, week = nflgame.live.current_year_and_week()
games = nflgame.live.current_games(year, week)
logging.info("Current year: " + str(year))
logging.info("Current week: " + str(week))
logging.info("Active games: " + str(games))

#If we find a Bills game in the active list, grab the game object and start a loop to watch the game to determine whether or not it has ended (ie. use if game.game_over() or while game.playing(self)). Once it has ended, 
#submit the post-game thread and then exit the loop. We should have this script (or the code iteself) executed one hour after the game thread is posted.

#Some other things that could be nice:
#game.nice_score(self), Returns a string of the score of the game. e.g., "NE (32) vs. NYG (0)".
