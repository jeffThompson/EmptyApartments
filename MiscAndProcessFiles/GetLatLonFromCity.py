
# -*- coding: utf-8 -*-

'''

https://pypi.python.org/pypi/geopy/1.9.1
'''

import csv
from geopy.geocoders import Nominatim

geolocator = Nominatim()
locations = []
reader = csv.reader(open('Craigslist_USCitiesWithLatLon.csv', 'rU'))

# read data, fill in gaps
for cl_name, print_name in reader:
	print '\n' + print_name
	try:
		results = geolocator.geocode(print_name)
		locations.append( [cl_name, print_name, results.latitude, results.longitude] )
		print '- ' + str(results.latitude) + '/' + str(results.longitude)
	except:
		locations.append( [cl_name, print_name, '', ''] )
		print '- couldn\'t find lat/lon!'

# write back out to file
print '\n\nWriting to file...'
writer = csv.writer(open('Craigslist_USCitiesWithLatLon.csv', 'w'))
writer.writerows(locations)

# done
print 'DONE!'

