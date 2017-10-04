
'''
GET ALL IMAGE WIDTHS
Jeff Thompson | 2016 | jeffreythompson.org

Utility to get total and mean width for all images.

'''

from PIL import Image

total_width = 0
num_imgs = 0
with open('../ApartmentImages/AllApartments_RANDOMIZED.txt') as f:
	print 'getting widths from images...'
	for i, line in enumerate(f):
		if i % 100 == 0:
			print '-', i
		try:
			img = Image.open(line.strip())
			width = img.size[0]
			total_width += width
			num_imgs += 1
		except:
			print '- error loading image (' + line + ')'

print '\ntotal width:', total_width, 'px'
print '# images:   ', num_imgs
print 'mean width: ', total_width/num_imgs, 'px'

