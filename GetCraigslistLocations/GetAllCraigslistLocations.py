
import requests, re, urllib, os
from bs4 import BeautifulSoup

'''
GET ALL CRAIGSLIST LOCATIONS
Jeff Thompson | 2015 | www.jeffreythompson.org

A script that creates a CSV file of all Craigslist
locations in the US. Attempts to add median income
by location by state; if it can't parse the location
it will ask for user input.

'''

prev_city = 		 'hattiesburg'							# for jumping ahead
output_filename =    'Craigslist_USCities.csv'				# file to save to
url = 				 'https://geo.craigslist.org/iso/us'	# CL URL to pull from
del_line =   		 '\x1b[1A'								# for fancy Terminal stuff


# jump ahead?
if prev_city != None:
	offset_found = False
	print 'Loading previous data...'
	with open(output_filename) as f:
		s = f.read()
else:
	offset_found = True
	s = 'city,alt_name,state,median_income,monthly_income,rent\n'


# load up median income data
print 'Loading median income by state...'
income = {}
with open('../Data/MedianIncome_2014.csv') as data:
	next(data)
	for listing in data:
		d = listing.strip().split(',')
		income[d[0]] = d[1]


# get all CL cities
print 'Getting all Craigslist cities...'
url = url.encode('utf-8')
html = requests.get(url).text
cities = re.findall('<li><a href="//(.*?)\.craigslist\.org/">', html)
print '- found ' + str(len(cities)) + ' cities!'


# get data
for i, city in enumerate(cities):

	# jump ahead
	if not offset_found:
		if city.lower() == prev_city.lower():
			offset_found = True
		continue
	
	print '\n' + str(i+1) + '/' + str(len(cities)) + ': ' + city

	# state
	url = 'http://' + city + '.craigslist.org'
	r = requests.get(url)
	title = re.search('<title>craigslist: .*?, ([A-Z]+) .*?</title>', r.text)
	wiki = re.search('http://en.wikipedia.org/wiki/.*?%2C_(.*?)"', r.text)
	if title != None:
		state = title.group(1)
	elif wiki != None:
		state = wiki.group(1)
	else:
		state = raw_input('...')
		print del_line + del_line

	# name listed at top of page
	title = re.search('<nav id="topban">.*?<h2>(.*?)<', r.text)
	if title != None:
		alt_name = title.group(1)
		l = [ word[0].upper() + word[1:] for word in alt_name.split() ]
		alt_name = ' '.join(l)
	else:
		alt_name = ''

	# median income
	yearly_income = int(income[state])
	monthly_income = int(yearly_income / 12)
	rent = int(monthly_income * 0.3)
	print '- ' + state + ', $' + yearly_income

	# store it
	s += city + ',"' + alt_name + '",' + state + ',' + str(yearly_income) + ',' + str(monthly_income) + ',' + str(rent) + '\n'
	with open(output_filename, 'w') as f:
		f.write(s)

print '\n' + 'ALL DONE!' + '\n\n'

