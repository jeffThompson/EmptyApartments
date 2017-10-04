
'''
EXTRACT FEATURES
Jeff Thompson | 2017 | jeffreythompson.org

Loads a folder of images and extracts their contents as PCA/t-SNE-ready
numpy arrays, saving the data out to an easily-readable HDF5 file. This 
process is reasonably fast, even with 100k images, though your output
file will be quite large (approx 7GB with stacked 64x64px images).

Based on these great samples from Gene Kogan and Kyle McDonald, though neither
worked well for me with larger datasets:

+ https://github.com/ml4a/ml4a-guides/blob/master/notebooks/image-search.ipynb
+ https://github.com/ml4a/ml4a-guides/blob/master/notebooks/image-tsne.ipynb
+ https://github.com/kylemcdonald/ImageRearranger/blob/master/Image%20Rearranger.ipynb

Plus tons and tons of Google and Stack Overflow searches :)

This code has been optimized for larger datasets that choked the examples
listed above. Attempts to prevent copying arrays or converting from Python lists
to numpy arrays are especially important here.

'''

import os 							# for getting filenames
import sys
import numpy as np 					# everything here is an array, really :)
from skimage.io import imread 		# for reading image data in
from skimage.color import gray2rgb
import h5py							# saving features to file (much better for large
									# datasets than csv would be)


# path to image filename
filename_path = '../ApartmentImages/64x64/Combo-NoDupes'

# filename to store extracted vectors in
output_filename = 'data/Features.h5'


# oh hey
term_width, term_cols = os.popen('stty size', 'r').read().split()
term_width = int(term_width)
print 'EXTRACT FEATURES FROM IMAGES'


# get a list of all image files, recursively, inside our source folder
print 'getting image filenames...'
filenames = [ [dp, f] for dp, dn, filenames in os.walk(filename_path) for f in filenames if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]


# get the number of images and their dimensions
num_images = len(filenames)
img = imread(os.path.join(filenames[0][0], filenames[0][1]))
px_w = img.shape[0]
px_h = img.shape[1]
channels = 3 			# rgb images have three channels
print '- found ' + str(num_images) + ' total images (' + str(px_w) + 'x' + str(px_h) + ' px each)'


# save filenames to file
print 'saving filenames to hdf5 file...'
f = h5py.File(output_filename, 'w')
f.create_dataset('labels', data=[ os.path.join(subfolder, filename) for (subfolder, filename) in filenames ], compression='gzip')
print '- done'


# load all those images one-by-one and convert them into a 
# normalized numpy array that we can use later for training
print 'loading all image data (will take a long time)...'

# create an empty numpy array for our image data
# casting from a regular list to a numpy array with large
# datasets is really slow, so this saves a step later
images = np.empty([num_images, px_w, px_h, channels])
	
# iterate through all images, load and process
for i, (subfolder, filename) in enumerate(filenames):

	# fancy progress printing
	info = '- ' + str(i+1) + '/' + str(num_images) + ': ' + filename
	info += (' ' * (term_width-len(info)))
	sys.stdout.write('\r' + info)
	sys.stdout.flush()

	# read pixels from file and extract the data
	img = imread(os.path.join(subfolder, filename))
	try:
		img = img[:,:,:3]					# no alpha channel, please
	except:
		img = gray2rgb(img, alpha=False)	# if image grayscale, convert to rgb
	images[i] = img.astype(np.float32)		# no need for super precision
											# (which also = bigger data file)


# we don't need the filenames anymore, so delete
# the array to save some memory (might not be necessary,
# but can't hurt either)
del filenames


# normalize image data to range of 0-1
# (instead of 0-255, also ensures we don't have skewed pixel
# data, like we'd get training on night-vision images, for example)
print '\n' + 'normalizing data...'
images -= images.min()				# make lowest value 0
images /= images.max() 				# and divide by the max
print '- done'


# convert into 2D array (required later for tsne and/or pca)
print 'converting stack to a 2D array...'
images = images.reshape(images.shape[0], -1)
print '- done'


# save image stack to file too
print 'saving image stack to file...'
f.create_dataset('data', data=images, compression='gzip')
f.close()
print '- done'

print '\n' + 'ALL DONE!' + '\n\n'

