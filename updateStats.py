#!/usr/bin/python3

from getHTML import *
from dbMethods import createDBConnection, updateDBSeason

TeamsFileName = 'teams.txt'
DBFileName = 'stats.db'

if __name__ == '__main__':
  
  # open the file containing all the team urls and names
  teams = open( TeamsFileName, 'r' )
  teamsList = teams.readlines() # get a list of all lines in the file
  teams.close()

  # open a connection to the database
  dbConn = createDBConnection( DBFileName )
  
  # for every team, get their current season's stats
  for team in teamsList:

    # file is in CSV format, so split line on the commas 
    teamSplit = team.split(',')
    # get the current season by passing the team's URL
    season = getCurrentSeason( teamSplit[0] )
    # insert the team's name at the beginning of each row
    for row in season:
      row = row.insert( 0, teamSplit[1] )

    # update the database with any new games 
    updateDBSeason( dbConn, season )



