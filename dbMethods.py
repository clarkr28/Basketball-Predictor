#!/usr/bin/python3

import sqlite3
from sqlite3 import Error

TableName = 'games'
DBFileName = 'gameData.db'

"""
open the database and make sure the database has the correct table created
param: fileName - the filename of the database
"""
def createDBConnection():

  # open a sqlite connection and get a cursor
  conn = sqlite3.connect( DBFileName )
  curs = conn.cursor()

  # try creating the table
  try:
    curs.execute('CREATE TABLE ' + TableName + ''' (SCHOOL TEXT NOT NULL, 
         SEASON INTEGER NOT NULL, GAME_NUM INTEGER NOT NULL, 
         DATE TEXT NOT NULL, LOCATION TEXT NOT NULL, OPPONENT TEXT NOT NULL, 
         GAME_RESULT TEXT NOT NULL, SCHOOL_PTS INTEGER NOT NULL, 
         OPPONENT_PTS INTEGER NOT NULL, SFG INTEGER NOT NULL,
         SFGA INTEGER NOT NULL, SFGP REAL NOT NULL, S3P INTEGER NOT NULL, 
         S3PA INTEGER NOT NULL, S3PP REAL NOT NULL, SFT INTEGER NOT NULL, 
         SFTA INTEGER NOT NULL, SFTP REAL NOT NULL, SORB INTEGER NOT NULL, 
         STRB INTEGER NOT NULL, SAST INTEGER NOT NULL, SSTL INTEGER NOT NULL, 
         SBLK INTEGER NOT NULL, STOV INTEGER NOT NULL, SPF INTEGER NOT NULL,
         OFG INTEGER NOT NULL, OFGA INTEGER NOT NULL, OFGP REAL NOT NULL, 
         O3P INTEGER NOT NULL, O3PA INTEGER NOT NULL, O3PP REAL NOT NULL, 
         OFT INTEGER NOT NULL, OFTA INTEGER NOT NULL, OFTP REAL NOT NULL, 
         OORB INTEGER NOT NULL, OTRB INTEGER NOT NULL, OAST INTEGER NOT NULL, 
         OSTL INTEGER NOT NULL, OBLK INTEGER NOT NULL, OTOV INTEGER NOT NULL, 
         OPF INTEGER NOT NULL, 
         PRIMARY KEY(SCHOOL, SEASON, GAME_NUM) ) ''' )
  except Error as e:
    # an error will be thrown if the table already exists
    print(e)

  conn.commit() # commit changes

  return conn



"""
insert any new games from the season into the database.  
param: dbConn - a connection to the database
param: fullSeasonData - a 2D list of all games in a season for a given team
return: number of games added to the database
"""
def updateDBSeason( conn, fullSeasonData ):

  # if the season data is empty, return
  if len(fullSeasonData) == 0:
    return

  schoolName = fullSeasonData[0][0]
  seasonYear = fullSeasonData[0][1]
  curs = conn.cursor()

  # get the most recent game stored in the database (highest game number)
  query = 'SELECT GAME_NUM FROM ' + TableName + \
      ' WHERE SCHOOL=? AND SEASON=? ORDER BY GAME_NUM DESC'
  curs.execute( query, (schoolName, seasonYear) )

  gameNums = curs.fetchall()
  gameNumMax = 0 if len(gameNums) == 0 else gameNums[0][0]

  # find all of the games that need to be added to the database
  gamesToAdd = [game for game in fullSeasonData if game[2] > gameNumMax]

  if len( gamesToAdd ) > 0:
    # add the games to the database
    query = 'INSERT INTO ' + TableName + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,' + \
        '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' 
    try:
      curs.executemany( query, gamesToAdd )
    except Error as e:
      print( 'error in dbMethods::updateDBSeason' )
      print( e )

  conn.commit()
  curs.close()

  return len( gamesToAdd )



"""
insert an entire season into the database
param1: conn, the database connection
param2: fullSeasonData, the team's entire season data
"""
def addFullSeason( conn, fullSeasonData ):

  curs = conn.cursor()
  query = 'INSERT INTO ' + TableName + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,' + \
      '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' 
  try:
    curs.executemany( query, fullSeasonData )
  except Error as e:
    print( 'error in dbMethods::addFullSeason' )
    print( e )

  conn.commit()
  curs.close()

  return



"""
get a game based on the school name, year, and game number
param
return list of stats for the game
"""
def getGameByNumber( conn, schoolName, year, gameNumber ):

  curs = conn.cursor()
  query = 'SELECT * FROM ' + TableName + \
      ' WHERE SCHOOL=? and SEASON=? and  GAME_NUM=?'
  curs.execute( query, (schoolName, year, gameNumber) )

  return curs.fetchall()

