#!/usr/bin/python3

import requests
from basketballHTMLParser import *
urlStart = 'https://www.sports-reference.com/cbb/schools/'
urlEnd = '/2018-gamelogs.html'

"""
gets the current season data for a specified team
parameter: the url for the team in sports-reference.com's website
return: table where each row contains the stats for a game
"""
def getCurrentSeason( teamUrl ):
  response = requests.get( urlStart + teamUrl + urlEnd )
  parser = GamelogHTMLParser()
  parser.feed( response.text )
  return parser.getTable()
