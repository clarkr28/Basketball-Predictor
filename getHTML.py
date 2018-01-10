#!/usr/bin/python3

import requests
from basketballHTMLParser import *
from schoolsHTMLParser import *

UrlSchools = 'https://www.sports-reference.com/cbb/schools/'
GamelogTag = '-gamelogs.html'

"""
gets the season data for a specified team and year
param: teamUrl str - the url for the team in sports-reference.com's website
param: year int - the season year to retrieve
return: table where each row contains the stats for a game
"""
def getSeason( teamUrl, year ):
  response = requests.get( UrlSchools + teamUrl + '/' + str(year) + GamelogTag )
  parser = GamelogHTMLParser()
  parser.feed( response.text )
  table = parser.getTable()     # get the final table from the parser

  # insert the season year at the front of the table
  for row in table:
    row = row.insert( 0, year )

  return table



"""
returns a table containing all of the schools on the sports-reference.com
page for basketball
"""
def getSchools():

  # make the get request to get the HTML
  response = requests.get( UrlSchools )
  # create the parser and feed the response into the parser
  parser = SchoolsHTMLParser()
  parser.feed( response.text )
  # get the final table from the parser
  table = parser.getTable()
  # return the table
  return table
