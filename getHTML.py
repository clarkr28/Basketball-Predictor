#!/usr/bin/python3

import requests
from basketballHTMLParser import *
url = 'https://www.sports-reference.com/cbb/schools/michigan-state/2018-gamelogs.html'

response = requests.get( url )
parser = GamelogHTMLParser()
parser.feed( response.text )
table = parser.getTable()
print( table )
