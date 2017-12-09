#!/usr/bin/python3

from html.parser import HTMLParser
from enum import Enum

class ParserState(Enum):
  # define all of the states
  NotInTable = 1
  InTable = 2 
  InRow = 3


class GamelogHTMLParser(HTMLParser):

  # id of the table
  TableId = 'sgl-basic'

  # True if the parsing is inside the table, False otherwise
  inTable = False

  # holds the state of where the parser is
  currState = ParserState.NotInTable

  # holds the data for the current row
  rowData = []

  # all of the data for the team's season
  seasonData = []

  # return the entire data table
  def getTable(self):
    return self.seasonData

  def handle_starttag(self, tag, attrs):

    # if not in a table, check to see if current tag is for a table
    if self.currState == ParserState.NotInTable:
      if tag == 'table':
        # make sure the table id is the correct id
        for att in attrs:
          if att[0] == 'id' and att[1] == self.TableId:
            # id is correct, so update current state
            self.currState = ParserState.InTable
            print('start tag:', tag)

		
  def handle_endtag(self, tag):

    # if already in a table, check to see if it's the end of a table
    if self.currState == ParserState.InTable:
      # see if the current tag is a table
      if tag == 'table':
        self.currState = ParserState.NotInTable # no longer in the table
        print("end tag  :", tag)


  def handle_data(self, data):

    if self.currState == ParserState.InTable:
      print(data)
