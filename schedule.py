#!/usr/bin/env python2.7
import sys
import urllib2
import xml.dom.minidom as xml
import shelve
import logging

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

# Use a modified version of the legacy nflgame schedule import script to load
# all Bills games info into a dictionary and store it within a shelve. The dictionary will 
# be used to determine when it is time to create gameday threads, how to title them, etc.

xml_base_url = 'http://www.nfl.com/ajax/scorestrip?'
start_year = 2018 # Years before 2009 don't seem to have JSON feeds.
end_year = 2018
team = 'BUF'
season_types = (
    ('PRE', xrange(1, 4 + 1)),
    ('REG', xrange(1, 17 + 1)),
    ('POST', [18, 19, 20, 22]),
)
schedule = shelve.open('bb-schedule.db')

logging.info("Beginning data retrieval...")

for year in xrange(start_year, end_year + 1):
    for season_type, weeks in season_types:
        for week, real_week in enumerate(weeks, 1):
            url = '%sseason=%d&seasonType=%s&week=%d' \
                  % (xml_base_url, year, season_type, real_week)
            try:
                dom = xml.parse(urllib2.urlopen(url))
            except urllib2.HTTPError:
                logging.info('Could not load %s' % url)
                continue

            for g in dom.getElementsByTagName("g"):
                eid = g.getAttribute('eid')
                home = g.getAttribute('h')
                away = g.getAttribute('v')
                
                #A hack to deal with the fact that the nfl XML doesn't provide 24 hour times and we can't assume that all times
                # are PM since Buffalo will play Jacksonville in Londan this year at 9AM EST.
                #if home == 'JAC':
                #    gameTime = unicode(g.getAttribute('t') + ' AM')
                #    preGamePosted = False
                #else:
                #    gameTime = unicode(g.getAttribute('t') + ' PM')
                #    preGamePosted = False
                
                gameTime = unicode(g.getAttribute('t') + ' PM')
                preGamePosted = False

                info = {
                    'eid': eid,
                    'wday': g.getAttribute('d'),
                    'year': int(eid[:4]),
                    'month': int(eid[4:6]),
                    'day': int(eid[6:8]),
                    'time': gameTime,
                    'season_type': season_type,
                    'week': week,
                    'home': home,
                    'away': away,
                    'gamekey': g.getAttribute('gsis'),
                    'preGamePosted': preGamePosted,
                    'gameDayPosted': False,
                    'postGamePosted': False
                }

                gameinfo = ((year, season_type, week, home, away), info)

                if home==team or away==team:
                    key = season_type + str(week)
                    logging.info(info)
                    logging.info('Storing ' + key)
                    schedule[key] = info

#Add an entry for testing
info = {
    'eid': '2015081452',
    'wday': 'Tues',
    'year': 2018,
    'month': 5,
    'day': 15,
    'time': unicode('5:05 PM'),
    'season_type': 'REG',
    'week': 0,
    'home': 'BUF',
    'away': 'PIT',
    'gamekey': '56767',
    'preGamePosted': False,
    'gameDayPosted': False,
    'postGamePosted': False
}
key = 'REG0'
logging.info(info)
logging.info('Storing ' + key)
schedule[key] = info

logging.info('Retrieval complete. Exiting...')
schedule.close()
