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

#BASE_URL = "http://www.imdb.com"

#time.sleep(1) for 1 second delay
#time.sleep(1) for 1 second delay

def compare(search_type, link1, link2):
	#title1 = raw_input("Enter full URL for title1: ")
	#title2 = raw_input("Enter full URL for title2: ")

	if search_type == "film":	
		# Get actor links for titles, or title links for actors
		results1, dic1 = get_actor_links(link1)
		# Sleep after any operation that gets from imdb, to prevent hammering the server
		time.sleep(0.5)
		results2, dic2 = get_actor_links(link2) # For now, dic2 is useless.
	elif search_type == "cast":
		results1, dic1 = get_movie_links(link1)
		time.sleep(0.5)
		results2, dic2 = get_movie_links(link2) # For now, dic2 is useless.
	else:
		return "Error: incorrect or no search type specified"

	#dups = find_dups(results1, results2, dic1)
	return find_dups(results1, results2, dic1)

def get_actor_links(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.text, "lxml")
	credits = soup.find("div", "header") # Not working; all links are returned 
	links = [a.attrs.get('href') for a in credits.select('tr a[href^=/name]')]
	names = [a.get_text() for a in credits.select('tr a[href^=/name]')]
	# This for loop removes extraneous info from end of links with a regular expression
	for i in range(len(links)):
		link_col = re.findall("/name/nm.......", links[i])
		links[i] = link_col[0]
	dic = dict(zip(links, names))
	return list(OrderedDict.fromkeys(links)), dic
	
def get_movie_links(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.text, "lxml")
	credits = soup.find("div", "filmography") # Not working; all links are returned 
	links = [a.attrs.get('href') for a in credits.select('a[href^=/title]')]
	names = [a.get_text() for a in credits.select('a[href^=/title]')]
	# This for loop removes extraneous info from end of links with a regular expression
	for i in range(len(links)):
		link_col = re.findall("/title/tt.......", links[i])
		links[i] = link_col[0]
	dic = dict(zip(links, names))
	return list(OrderedDict.fromkeys(links))

def find_dups(list1, list2, dict0):
	duptitles = []
	duplinks = []
	# This can be improved in any number of ways. They're ordered lists, after all!
	for link in list1:
		if link in list2:
			duptitles.append(link)
			duplinks.append(dict0[link])
	return dict(zip(duptitles,duplinks))

def get_titles(dups, dic):
	titles = []
	for link in dups:
		titles.append(dic[link])
	return titles
