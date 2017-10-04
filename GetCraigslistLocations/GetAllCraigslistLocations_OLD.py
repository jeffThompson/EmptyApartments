
import requests, re, urllib, os
from bs4 import BeautifulSoup

'''
GET ALL CRAIGSLIST LOCATIONS
Jeff Thompson | 2015 | www.jeffreythompson.org

Get a URL-ready list of all Craigslist locations around
the world.

'''

#location_filename = 'AllCraigslistLocations.txt'
location_filename =  'USCities.txt'
url = 				 'https://geo.craigslist.org/iso/us'


# download locations page from CL
print 'Downloading from Craigslist...'
url = url.encode('utf-8')
r = requests.get(url)
soup = BeautifulSoup(r.text)


# extract all locations
print 'Extracting locations...'
locations = []
for a in soup.find_all('a', href=True):
	url = re.search(r'http://([a-z].*?)\.craigslist\.org', a['href'])
	if url != None:
		locations.append(url.group(1))
print '- found ' + str(len(locations)) + ' locations!'


# save to file
print 'Saving to file...'
with open(location_filename, 'w') as f:
	for location in locations:
		f.write(location + '\n')


# done!
print '\n' + 'ALL DONE!' + '\n\n'

