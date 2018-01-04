#!/usr/bin/python3

import requests
from basketballHTMLParser import *

CurrentSeasonYear = 2018
UrlStart = 'https://www.sports-reference.com/cbb/schools/'
UrlEnd = '/' + str(CurrentSeasonYear) + '-gamelogs.html'

"""
gets the current season data for a specified team
parameter: the url for the team in sports-reference.com's website
return: table where each row contains the stats for a game
"""
def getCurrentSeason( teamUrl ):
  response = requests.get( UrlStart + teamUrl + UrlEnd )
  parser = GamelogHTMLParser()
  parser.feed( response.text )
  table = parser.getTable()     # get the final table from the parser

  # insert the season year at the front of the table
  for row in table:
    row = row.insert( 0, CurrentSeasonYear )

  return table
