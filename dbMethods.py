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
    print('error in dbMethods::createDBConnection')
    print(e)

  conn.commit() # commit changes

  return conn



"""
insert any new games from the season into the database.  
param: dbConn - a connection to the database
param: fullSeasonData - a 2D list of all games in a season for a given team
"""
def updateDBSeason( conn, fullSeasonData ):

  # for now, just insert the entire season into the database
  curs = conn.cursor()
  query = 'INSERT INTO ' + TableName + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,' + \
      '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)' 
  try:
    curs.executemany(query, fullSeasonData)
  except Error as e:
    print('error in dbMethods::updateDBSeason')
    print(e)

  conn.commit()
  curs.close()

  return
