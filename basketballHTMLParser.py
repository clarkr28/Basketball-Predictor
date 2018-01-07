#!/usr/bin/python3

from html.parser import HTMLParser
from enum import Enum


# return true if the string passed to the function is a float
def isFloat(x):
  try:
    a = float(x)
  except ValueError:
    return False
  else:
    # search the string for a decimal point to make sure it's not an integer
    return x.find('.') != -1


# return true if the string passed to the function is an integer
def isInt(x):
  try:
    a = int(x)
  except ValueError:
    return False
  else:
    # search the string for a decimal point to make sure it's not a float
    return x.find('.') == -1



class ParserState(Enum):
  # define all of the states
  NotInTable = 1
  InTable = 2 
  InTableBody = 3
  InRow = 4
  InSmall = 5
  InOpponent = 6



class GamelogHTMLParser(HTMLParser):

  # id of the table
  TableId = 'sgl-basic'

  # id of the opponent cell
  OpponentId = 'opp_id'

  # full size of a row
  FullRowSize = 39

  # True if there was a link to the opponent's page - if there was no link, 
  # that means sports-reference.com does not have data for that team.  If this
  # is the case, don't add the game to the season's data b/c there is no way 
  # to get more information about the team
  opponentLinkFound = False

  # holds the state of where the parser is
  currState = ParserState.NotInTable

  # holds the data for the current row
  rowData = []

  # all of the data for the team's season
  seasonData = []

 
  # initialization
  def __init__(self):

    HTMLParser.__init__(self)  # call the base class initialization 

    # id of the table
    self.TableId = 'sgl-basic'

    # id of the opponent cell
    self.OpponentId = 'opp_id'

    # full size of a row
    self.FullRowSize = 39

    # initialize to false
    self.opponentLinkFound = False

    # holds the state of where the parser is
    self.currState = ParserState.NotInTable

    # holds the data for the current row
    self.rowData = []

    # all of the data for the team's season
    self.seasonData = []
  


  # return the entire data table
  def getTable(self):
    return self.seasonData



  def handle_starttag(self, tag, attrs):

    # if not in a table and the current tag is a table, make sure this is 
    # the correct table by checking the table id.
    if self.currState == ParserState.NotInTable and tag == 'table':
      # make sure the table id is the correct id
      for att in attrs:
        if att[0] == 'id' and att[1] == self.TableId:
          # id is correct, so update current state
          self.currState = ParserState.InTable

    # move current state to in table body if necessary
    elif self.currState == ParserState.InTable and tag == 'tbody':
      self.currState = ParserState.InTableBody

    # move current state to in row if necessary
    elif self.currState == ParserState.InTableBody and tag == 'tr':
      self.currState = ParserState.InRow

    # move current state to small if necessary
    elif self.currState == ParserState.InRow and tag == 'small':
      self.currState = ParserState.InSmall

    # move current state to inOpponent if necessary
    elif self.currState == ParserState.InRow and tag == 'td':
      # see if the cell id is the opponent id
      for att in attrs:
        if att[0] == 'data-stat' and att[1] == self.OpponentId:
          self.currState = ParserState.InOpponent

    # if current state is in opponent and tag is a link, add href to data row
    elif self.currState == ParserState.InOpponent and tag == 'a':
      for att in attrs:
        if att[0] == 'href':
          # append only the school name from the href - should be in the
          # format '/cbb/schools/school-name/year.html'
          self.rowData.append( att[1].split('/')[3] )
          # remember that we found the opponent link for later
          self.opponentLinkFound = True


		
  def handle_endtag(self, tag):

    # if currently in a table and the current tag is a table, set the current
    # state to not being in a table.
    if self.currState == ParserState.InTable and tag == 'table':
      self.currState = ParserState.NotInTable # no longer in the table

    # if currently in the table body and the current tag is is tbody, set the
    # current state to being in a table.
    elif self.currState == ParserState.InTableBody and tag == 'tbody':
      self.currState = ParserState.InTable

    # if currently in a row and current tag is a (table row), set the 
    # current state to being in a table body, then insert the completed row
    # into the season data list
    elif self.currState == ParserState.InRow and tag == 'tr':
      self.currState = ParserState.InTableBody

      # a home game leaves the game location field blank, which does not get
      # added to the list.  So if the size of the list is 1 smaller than it
      # should be, insert a 'H' into the row to show it as a home game.
      if len( self.rowData ) == self.FullRowSize - 1:
        self.rowData.insert(2, 'H')

      # only append the game to the season if the opponent link was found and
      # the row is the correct size (there are instances where values are
      # missing, don't add these games to the season)
      if self.opponentLinkFound == True and \
          len(self.rowData) == self.FullRowSize:
        self.seasonData.append(self.rowData) # append entire row to season data
        self.opponentLinkFound = False       # reset back to false

      self.rowData = []                    # set to empty for next row

    # if currently in small and the endtag is small, change state to InRow
    elif self.currState == ParserState.InSmall and tag == 'small':
      self.currState = ParserState.InRow

    # if currently in opponent field and endtag is td, change to InRow
    elif self.currState == ParserState.InOpponent and tag == 'td':
      self.currState = ParserState.InRow



  def handle_data(self, data):

    # if currently in a row, save the data to the row list
    if self.currState == ParserState.InRow:
      # if the data is an integer, put it in the list as in integer
      if isInt(data):
        self.rowData.append( int(data) )
      # if the data is a float, put it in the list as a float
      elif isFloat(data):
        self.rowData.append( float(data) )
      # if neither an int or float, leave data as a string
      else:
        self.rowData.append( data )
