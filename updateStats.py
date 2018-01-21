#!/usr/bin/python3

from getHTML import getSeason
from dbMethods import createDBConnection, updateDBSeason

TeamsFileName = 'allSchools.txt'

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
    season = getSeason( team, 2018 ) # get the current season by for the team

    # if there are games in the season, update the database with new games
    gamesAdded = 0
    if len( season ) > 0:
      gamesAdded = updateDBSeason( dbConn, season )

    # print the team name and year of the team
    print( season[0][0], season[0][1], gamesAdded )


  # close the database connection
  dbConn.close()
