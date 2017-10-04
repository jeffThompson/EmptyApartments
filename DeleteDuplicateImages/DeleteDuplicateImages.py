
'''
REMOVE DUPLICATE IMAGES
Jeff Thompson | 2017 | jeffreythompson.org

Loads all images in a folder (including subfolders) and
computes their "distance" hash. This, with the filename,
is saved to a Python shelve database for later parsing.

Then goes through the database, makes a list of duplicate
images, and, if specified, moves them to a new folder.

- - -

Hash stuff mostly via: https://realpython.com/blog/python/
fingerprinting-images-for-near-duplicate-detection/

A "distance" hash, or "locality-sensitive" hash, works by
reducing the data so that similar items map to the same
hash with a high probability. This is the opposite of
cryptographic hashing, where tiny differences should result
in a really different hash. 

More info: https://en.wikipedia.org/wiki/Locality-sensitive_hashing

'''

from PIL import Image
import imagehash, shelve, os


# folder of images to work with (can be in subfolders)
image_path = '../ApartmentImages/64x64/Combo-NoDupes'

# database file to save to
# (automatically gets .db extension)
db_filename =        'hashes'

# listings of unique and duplicate images
unique_filename =    'unique.csv'
duplicate_filename = 'duplicates.csv'

# move dupes?
move_duplicates =    True
dupe_path = 		 '../ApartmentImages/DUPES_64x64_Combo'


# create a shelve database for image hashes
# delete any data that might be in there, too
print 'creating empty database...'
db = shelve.open( db_filename, writeback=True)
db.clear()


# get a list of all image files, recursively, inside our source folder
print 'getting image filenames...'
filenames = [ os.path.join(dp, f) for dp, dn, filenames in os.walk(image_path) for f in filenames if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]
num_files = len(filenames)
print '- found ' + str(num_files) + ' images'


# do it
print 'hashing images (may take a while)...'
for i, path in enumerate(filenames):
	# print str(i+1) + ' / ' + str(num_files)

	# load image, compute hash difference
	img = Image.open(path)
	h = str( imagehash.dhash(img))

	# add to the database
	# hash is the key, file path gets added to a list of values
	db[h] = db.get(h, []) + [path]

print '  - done'


# look for hashes with more than one entry
print 'getting list of unique images...'
unique_files = []
duplicates = []
for i, key in enumerate(db.keys()):
	# print str(i+1) + ' / ' + str(len(db.keys()))

	# get list of files for this hash
	filenames = db[key]
	
	# if more than one file, add all to duplicates list
	if len(filenames) > 1:
		duplicates.append(filenames)
	
	# either way, add the first value (gets *all* unique images)
	unique_files.append(filenames[0])
print '- found ' + str(len(duplicates)) + ' duplicate images!'


# optional: move duplicate images
if len(duplicates) > 0 and move_duplicates:
	print 'moving duplicates...'
	
	# create path for dupe folder, if necessary
	if not os.path.exists(dupe_path):
		os.mkdir(dupe_path)

	# keep first dupe image, move the rest
	for filenames in duplicates:
		for filename in filenames[1:]:
			name = os.path.basename(filename)
			os.rename(filename, os.path.join(dupe_path, name))
	print '- done'


# save lists to file
print 'saving lists to file...'
with open(unique_filename, 'w') as f:
	f.write( '\n'.join(unique_files) )
with open(duplicate_filename, 'w') as f:
	for filenames in duplicates:
		f.write( ','.join(filenames) + '\n' )


print 'ALL DONE!'
db.close()
exit()

