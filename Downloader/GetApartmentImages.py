# -*- coding: utf-8 -*-

import argparse, requests, re, urllib, os, csv, shutil
from bs4 import BeautifulSoup

'''
GET APARTMENT IMAGES
Jeff Thompson | 2015-16 | www.jeffreythompson.org

Auto-download images of empty apartments from Craigslist.

OPTIONAL ARGS:
-p, --page 			how many listings to offset?
-d, --search_depth 	how many pages of listings to return (default 0)
--median 			cap search at median income?
--graphics_thresh 	threshold for graphical images (low entropy = likely
					graphics; default 3.9)
--photo_thresh 		threshold for photographic images (high entropy = likely
					photo; default 4.4)
--prev_location 	skip ahead to previous location, listed as CL location name
-q, --quiet 		suppress all output from program

REQUIRES:
BeautifulSoup for parsing HTML
ImageMagick for testing entropy

MEDIAN INCOME DATA SOURCE:
http://factfinder.census.gov/faces/tableservices/jsf/
pages/productview.xhtml?src=bkmk

NOTES:
- may work better (ie less likely to get your IP locked
  out) if running from a .edu ISP

'''

# ==============

def find_apartments(location, offset, max_rent):
	if not quiet: print location.upper()

	# what is max rent?
	if use_median_income:
		if not quiet: print '- max rent $' + str(max_rent)
	else:
		if not quiet: print '- no rent cap'

	# make image folder if doesn't exist
	if not os.path.exists(location):
		os.makedirs(location)
	path = os.path.join(location, '_Graphics')
	if not os.path.exists(path):
		os.mkdir(path)
	path = os.path.join(location, '_Maybe')
	if not os.path.exists(path):
		os.mkdir(path)

	# get list of apartments
	if not quiet: print '\n' + 'Searching apartments...'
	apartments = []
	url = 'http://' + location + '.craigslist.org/search/hhh?s=' + str(offset)
	if use_median_income:
		url += '&maxAsk=' + str(max_rent)
	url += '&hasPic=1&query=apartment'
	url = url.encode('utf-8')
	if not quiet: print '- ' + url

	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	for a in soup.find_all('a', class_='hdrlnk', href=True):
		apartment_url = 'http://' + location + '.craigslist.org' + a['href']
		apartments.append(apartment_url)
	if len(apartments) == 0:
		if not quiet: print '- found no apartments, probably got blocked :('
		if not quiet: print '- quitting...' + '\n\n- - - - -\n'
		shutil.rmtree(location)
		exit(0)
	else:
		if not quiet: print '- found ' + str(len(apartments)) + ' apartments!'

	# download em all!
	total_image_count = 0
	for i, apartment in enumerate(apartments):

		# fix any url problems
		url = apartment.encode('utf-8')
		actual_url = re.search(r'craigslist\.org(http://.*?\.html)', url)
		if actual_url != None:
			url = actual_url.group(1)

		# did we reach end of listings?
		listed_location = re.search(r'http://([a-z].*?)\.craigslist\.', url)
		if listed_location != None and listed_location.group(1) != location:
			if not quiet: print '\n' + 'End of actual listings, done!'
			break

		# get all images from page
		if not quiet: print '\n' + str(i+1) + '/' + str(len(apartments)) + ': ' + url
		try:

			# get list of images
			images = []
			r = requests.get(url)
			image_list = re.findall(r'var imgList.*?;', r.text)
			images = re.findall(r'"url":"(.*?)"', image_list[0])
			total_image_count += len(images)

			# download (if we don't already have it)
			# if we think the image is graphics, place it in
			# a separate folder for review
			if not quiet: print '- Downloading ' + str(len(images)) + ' images...'
			for url in images:
				if not quiet: print '  - ' + url
				image_path = os.path.join(location, os.path.basename(url))
				if os.path.isfile(image_path) == False:
					urllib.urlretrieve(url, image_path)

				# get image entropy
				px = os.popen('convert -format "%w*%h\n" "' + image_path + '" info:|bc').read().strip()
				cmd = 'convert "' + image_path + '" -colorspace gray -depth 8 -format "%c" histogram:info:- | awk -F: -v px=' + px + ' \'{p=$1/' + px + ';e+=-p*log(p)} END {print e}\''
				entropy = float(os.popen(cmd).read().strip())

				# low entropy = graphics
				# move to separate folder
				if entropy < graphics_threshold:
					src = image_path
					dst = os.path.join(location, '_Graphics', os.path.basename(image_path))
					shutil.move(src, dst)

				# not sure = maybe
				# move to separate folder
				elif entropy >= graphics_threshold and entropy < photo_threshold:
					src = image_path
					dst = os.path.join(location, '_Maybe', os.path.basename(image_path))
					shutil.move(src, dst)

				# otherwise, leave in place

		# catch any errors downloading
		except Exception, e:
			if not quiet: print '- Error finding images, skipping...'
			# print str(e)

	# results
	if not quiet: print '\n' + 'Downloaded a total of ' + str(total_image_count) + ' images'
	if total_image_count == 0:
		if not quiet: print '- found no images, probably got blocked :('
		if not quiet: print '- quitting...' + '\n\n- - - - -\n'
		shutil.rmtree(location)
		exit(0)

# ==============

if __name__ == '__main__':
	p = argparse.ArgumentParser(description='Auto-download images of empty apartments from Craigslist.', usage='python GetApartmentImages.py [options]')
	p.add_argument('-p', '--page', type=int, default=0, help='how many listings to offset?', metavar='')
	p.add_argument('-d', '--search_depth', type=int, default=0, help='how many pages of listings to return (default 0)', metavar='')
	p.add_argument('--median', action='store_true', help='cap search at median income?')
	p.add_argument('--graphics_thresh', type=float, default=3.9, help='threshold for graphical images (low entropy = likely graphics; default 3.9)', metavar='')
	p.add_argument('--photo_thresh', type=float, default=4.4, help='threshold for photographic images (high entropy = likely photo; default 4.4)', metavar='')
	p.add_argument('--prev_location', help='skip ahead to previous location, listed as CL location name', metavar='')
	p.add_argument('-q', '--quiet', action='store_true', help='suppress all output from program')
	args = p.parse_args()

	page = args.page
	search_depth = args.search_depth
	use_median_income = args.median
	graphics_threshold = args.graphics_thresh
	photo_threshold = args.photo_thresh
	quiet = args.quiet

	previous_location = args.prev_location
	skip_ahead = False
	if previous_location != None:
		skip_ahead = True
	
	# do all cities!
	with open('Craigslist_USCities.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader, None)			# skip header
		for data in reader:
			city = 	  		 data[0]
			alt_name = 		 data[1]
			state =   		 data[2]
			max_rent = 		 int(data[5])

			# skip ahead until previous city
			if skip_ahead:
				if not quiet: print 'Skipping ' + city + '...'
				if city == previous_location:
					if not quiet: print '\n- - - - -\n'
					skip_ahead = False
				continue

			# get em
			for i in range(search_depth+1):
				find_apartments(city, (page+i)*100, max_rent)
			if not quiet: print '\n- - - - -\n'

	if not quiet: print 'ALL DONE' + '\n\n'

