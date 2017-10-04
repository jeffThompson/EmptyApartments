
'''
STACK IMAGES
Jeff Thompson | 2017 | jeffreythompson.org

Loads a set of images at varying blur levels and stacks them
into a single image for feature extraction. This method, as
opposed to loading them separately and combining the resulting
pixel arrays, turns out to be much faster, and removes the need
to re-combine the data if changes to the training script are
made.

PREPARE IMAGES
Images should be resized ahead of time: to avoid memory issues,
64x64 pixels seems to work well for large-ish datasets (100k images
with 16GB RAM). Resizing can be done using ImageMagick, even if
they are in subfolders:

	find . -name '*.jpg' -execdir mogrify -resize 64x64! {} \;

Two more copies of the images, in their own folders, should be made
the the images blurred at varying levels. Blurring can also be 
accomplished using ImageMagick. Blur levels of 3 and 8 seems to
work well for 64x64 pixel images:

	find . -name '*.jpg' -execdir mogrify -blur 0x3 {} \;
	find . -name '*.jpg' -execdir mogrify -blur 0x8 {} \;

When done, run this script to combine the images. The new image
files will be written to their own folder, preserving any directory
structure in the input files.

'''

import os 					# for getting lists of files
from PIL import Image 		# handles all the image stuff


# three folders with pre-prepped images
# should be resized and blurred already (see note about
# on settings)
not_blurred_path =  '../ApartmentImages/64x64/NotBlurred'
blurred_path =      '../ApartmentImages/64x64/Blurred'
very_blurred_path = '../ApartmentImages/64x64/VeryBlurred'

# output folder to save combined images to
# directory structure will get created, even if your input
# images are in sub-folders
output_path =       '../ApartmentImages/64x64/Combo'


# get a list of all image files, recursively, inside our source folder
print 'getting image filenames...'
filenames = [ [ os.path.split(dp)[1], f] for dp, dn, filenames in os.walk(not_blurred_path) for f in filenames if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]
num_files = len(filenames)
print '- found ' + str(num_files) + ' files'


# get input image dims (by loading the first image)
img = Image.open(os.path.join(not_blurred_path, filenames[0][0], filenames[0][1]))
width, height = img.size
print width, height


# for each file, load the three versions and combine
print 'combining all images...'
for i, (subfolder, filename) in enumerate(filenames):
	print '- ' + str(i+1) + '/' + str(num_files) + ': ' + os.path.join(subfolder, filename)
	
	# format paths to not blurred, blurred, and very blurred images
	nb = os.path.join(not_blurred_path, subfolder, filename)
	b =  os.path.join(blurred_path, subfolder, filename)
	vb = os.path.join(very_blurred_path, subfolder, filename)

	# open all of em at once (nice!)
	combo = map(Image.open, [ nb, b, vb ])
	
	# create output image, stack the input images vertically
	out = Image.new('RGB', (width, height*3))
	for i, img in enumerate(combo):
		out.paste(img, (0, i*height))

	# format output path and save
	output_dir = os.path.join(output_path, subfolder)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	out.save(os.path.join(output_dir, filename))

print 'all done!'

