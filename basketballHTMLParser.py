#!/usr/bin/python3

from html.parser import HTMLParser

class AdvancedGamelogHTMLParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      print('start tag:', tag)
      print('  - attrs:', attrs)
		
  def handle_endtag(self, tag):
    if tag == 'table':
      print("end tag  :", tag)
