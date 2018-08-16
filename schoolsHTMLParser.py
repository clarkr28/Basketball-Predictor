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



class SchoolsHTMLParser(HTMLParser):

    # id of the table
    TableId = 'schools'

    # holds the state of where the parser is
    currState = ParserState.NotInTable

    # holds the data for the current row
    rowData = []

    # all of the data for the team's season
    totalData = []

      # initialization
    def __init__(self):

        HTMLParser.__init__(self)  # call the base class initialization 

        # id of the table
        self.TableId = 'schools'

        # holds the state of where the parser is
        self.currState = ParserState.NotInTable

        # holds the data for the current row
        self.rowData = []

        # all of the data for the team's season
        self.totalData = []
    

    # return the entire data table
    def getTable(self):
        return self.totalData



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
            headerRow = False   # initialize to false
            for att in attrs:
                # there are header rows throughout the table, avoid them by 
                # checking the class labels
                if att[0] == 'class' and att[1] == 'thead':
                    headerRow = True

            if not headerRow:
                self.currState = ParserState.InRow

        # if we are in a row, check to see if the starttag is a link (a)
        elif self.currState == ParserState.InRow and tag == 'a':
            # find the href of the link and append it to the rowData
            for att in attrs:
                if att[0] == 'href':
                    # split the href by '/' and append the second to last section, 
                    # which is the part of the link that has the school's URL name.
                    self.rowData.append( att[1].split('/')[-2] )




    def handle_endtag(self, tag):

        # if currently in a table and the current tag is a table, set the current
        # state to not being in a table.
        if self.currState == ParserState.InTable and tag == 'table':
            self.currState = ParserState.NotInTable # no longer in the table

        # if currently in the table body and the current tag is is tbody, set the
        # current state to being in a table.
        elif self.currState == ParserState.InTableBody and tag == 'tbody':
            self.currState = ParserState.InTable

        # if currently in a row and current tag is a tr (table row), set the 
        # current state to being in a table body, then insert the completed row
        # into the season data list
        elif self.currState == ParserState.InRow and tag == 'tr':
            self.currState = ParserState.InTableBody

            self.totalData.append(self.rowData) # append entire row to season data
            self.rowData = []                    # set to empty for next row




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
