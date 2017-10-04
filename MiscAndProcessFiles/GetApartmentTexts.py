
# -*- coding: utf-8 -*-

'''
GET APARTMENT TEXTS
Jeff Thompson | 2015 | www.jeffreythompson.org

Auto-download apartment descriptions from Craigslist.

NOTES:
+	Average US household income is $50,500; should spend ~30%
	on rent – good base rent would be $1262.50/mo

'''

import requests, re, os
from bs4 import BeautifulSoup


max_rent = 	   		1262			# how much rent are you willing to pay in local currency?
page = 	   	   		0				# how many listings to offset? (0 = first page, 100 listings/page)
search_depth = 		0				# how many pages of listings to return (0 - N pages)

skip_ahead = 		False			# pick up where you left off?
previous_location = 'bellingham'	# and where is that?


def find_apartments(location, offset):

	# make image folder if doesn't exist
	if not os.path.exists(location):
		os.makedirs(location)

	# get list of apartments
	print location.upper()
	print 'Searching apartments...'
	apartments = []
	url = 'http://' + location + '.craigslist.org/search/hhh?s=' + str(offset) + '&maxAsk=' + str(max_rent) + '&hasPic=1&query=apartment'
	url = url.encode('utf-8')
	print '- ' + url
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	for a in soup.find_all('a', class_='hdrlnk', href=True):
		apartment_url = 'http://' + location + '.craigslist.org' + a['href']
		apartments.append(apartment_url)
	print '- found ' + str(len(apartments)) + ' apartments!'

	# download em all!
	for i, apartment in enumerate(apartments):

		# fix any url problems
		url = apartment.encode('utf-8')
		actual_url = re.search(r'craigslist\.org(http://.*?\.html)', url)
		if actual_url != None:
			url = actual_url.group(1)

		# did we reach end of listings?
		listed_location = re.search(r'http://([a-z].*?)\.craigslist\.', url)
		if listed_location != None and listed_location.group(1) != location:
			print '\n' + 'End of actual listings, done!'
			break

		# where we at?
		print '\n' + str(i+1) + '/' + str(len(apartments)) + ': ' + url
		try:

			# get list of images
			images = []
			r = requests.get(url)
			soup = BeautifulSoup(r.text)
			desc = soup.find('section', {'id': 'postingbody'}).text.strip()

			# add to file
			print '- Adding description to file...'
			with open('Descriptions/' + location + '.txt', 'a') as f:
				f.write(desc.encode('utf8') + '\n')

		# catch any errors downloading
		except Exception, e:
			print e
			print '- Error finding description, skipping...'


# just do all of them!
with open('Craigslist_USCities.txt') as cities:
	for city in cities:
		city = city.strip()

		# skip ahead until previous city
		if skip_ahead:
			print 'Skipping ' + city + '...'
			if city == previous_location:
				print '\n- - - - -\n'
				skip_ahead = False
			continue

		# get em
		for i in range(search_depth+1):
			find_apartments(city, (page+i)*100)
		print '\n- - - - -\n'

