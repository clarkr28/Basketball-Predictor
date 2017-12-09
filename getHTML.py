#!/usr/bin/python3

import requests
from basketballHTMLParser import *
url = 'https://www.sports-reference.com/cbb/schools/michigan-state/2017-gamelogs-advanced.html'

response = requests.get(url)
parser = AdvancedGamelogHTMLParser()
parser.feed(response.text)
