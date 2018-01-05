#!/usr/bin/python3

from getHTML import *
from dbMethods import createDBConnection, updateDBSeason

TeamsFileName = 'teams.txt'

if __name__ == '__main__':
  
  # open the file containing all the team urls and names
  teams = open( TeamsFileName, 'r' )
  teamsList = teams.readlines() # get a list of all lines in the file
  teams.close()

  # open a connection to the database
  dbConn = createDBConnection()
  
  # for every team, get their current season's games
  for team in teamsList:

    team = team.strip() # strip to avoid whitespace
    season = getCurrentSeason( team ) # get the current season by for the team
    # insert the team's name at the beginning of each row
    for row in season:
      row = row.insert( 0, team )

    # print the team name and year of the team
    print( season[0][0], season[0][1] )

    # update the database with any new games 
    updateDBSeason( dbConn, season )

  # close the database connection
  dbConn.close()

