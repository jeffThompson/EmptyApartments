
import requests, re, urllib, os
from bs4 import BeautifulSoup

'''
GET ALL CRAIGSLIST LOCATIONS
Jeff Thompson | 2015 | www.jeffreythompson.org


'''

prev_city = 		 None
output_filename =    'Craigslist_USCities.csv'
url = 				 'https://geo.craigslist.org/iso/us'
del_line =   		 '\x1b[1A'


s = [ 'city,alt_name,state,median_income,monthly_income,rent' ]
with open('Craigslist_USCities.csv') as f:
	next(f)
	for line in f:
		s.append(line.strip())


# get data
for i in range(0,len(s)):
	if i == 0:
		continue
	data = s[i].split(',')

	city = data[0]
	state = data[1]
	print city + ', ' + state
	url = 'http://' + city + '.craigslist.org'
	r = requests.get(url)

	# page title name
	title = re.search('<nav id="topban">.*?<h2>(.*?)<', r.text, re.DOTALL)
	if title != None:
		alt_name = title.group(1)
		l = [ word[0].upper() + word[1:] for word in alt_name.split() ]
		alt_name = '"' + ' '.join(l) + '"'
	else:
		alt_name = ''
	print '- ' + alt_name

	# median income
	yearly_income = int(data[2])
	monthly_income = int(yearly_income / 12)
	rent = int(monthly_income * 0.3)

	# store it
	s[i] = city + ',' + alt_name + ',' + state + ',' + str(yearly_income) + ',' + str(monthly_income) + ',' + str(rent)

with open(output_filename, 'w') as f:
	for city in s:
		f.write(city + '\n')

print '\n' + 'ALL DONE!' + '\n\n'
