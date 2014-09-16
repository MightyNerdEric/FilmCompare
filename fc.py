'''
Author: Eric Ball
E-mail: mightynerderic@gmail.com
Github: https://www.github.com/mightynerderic
'''

import requests
import time
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

BASE_URL = "http://www.imdb.com"

#time.sleep(1) for 1 second delay

#response = requests.get(BASE_URL + "/title/tt0103359/fullcredits?ref_=tt_cl_sm#cast")


def main():
	title1 = raw_input("Enter full URL for title1: ")
	title2 = raw_input("Enter full URL for title2: ")

	# Get actor links for titles, or title links for actors
	actors1 = get_actor_links(title1)
	print actors1
	# Sleep after any operation that gets from imdb, to prevent hammering the server
	time.sleep(1)
	actors2 = get_actor_links(title2)
	print actors2

	dups = find_dups(actors1, actors2)
	# dups now contains a set of links that were on both pages. Use XML to get info from those pages.
	titles = get_titles(dups)
	print titles

def get_actor_links(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.text, "lxml")
	# Not working; all links are returned
	credits = soup.find("div", "header")
	links = [a.attrs.get('href') for a in credits.select('tr a[href^=/name]')]
	# This for loop removes extraneous info from end of links with a regular expression
	for i in range(len(links)):
		link_col = re.findall("/name/nm.......", links[i])
		links[i] = link_col[0]
	return list(OrderedDict.fromkeys(links))

def find_dups(list1, list2):
	dups = []	
	# This can be improved in any number of ways. They're ordered lists, after all!
	for link in list1:
		if link in list2:
			dups.append(link)
	return dups

main()
