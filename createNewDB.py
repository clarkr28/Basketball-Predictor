#!/usr/bin/python3

from getHTML import getSeason
from dbMethods import createDBConnection, addFullSeason

TeamsFileName = 'allSchools.txt'

"""
The purpose of this script is to create and completely fill the database
"""

if __name__ == '__main__':

    # open the file containing the team urls
    teams = open( TeamsFileName, 'r')
    teamsList = teams.readlines() # get a list of all the lines in the file
    teams.close()

    # open a connection to the database
    dbConn = createDBConnection()

    # for every team, get their current season's games
    for team in teamsList:

        team = team.strip() # strip to avoid whitespace
        for year in range(2011, 2019):

            season = getSeason( team, year )

            # print the team name and year of the season
            print( team, year )

            # add all games to the database, if there are any
            if len( season ) > 0:
                addFullSeason( dbConn, season )

    # close the database connection
    dbConn.close()
