#!/usr/bin/python3

from getHTML import *

TeamsFileName = 'teams.txt'

if __name__ == '__main__':
  
  # open the file containing all the team urls and names
  teams = open( TeamsFileName, 'r' )
  teamsList = teams.readlines() # get a list of all lines in the file
  teams.close()
  
  # for every team, get their current season's stats
  for team in teamsList:

    # file is in CSV format, so split line on the commas 
    teamSplit = team.split(',')
    # get the current season by passing the team's URL
    season = getCurrentSeason( teamSplit[0] )

    # print the name of the team and the games played this season
    print( teamSplit[1], 'has played', len(season), 'games this season' )


