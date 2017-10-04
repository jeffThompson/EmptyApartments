
import os, glob, shutil

graphics_theshold = 3.9
photo_threshold = 	4.4
folder = 			'TestImages'
images = 	   		glob.glob(folder + '/*.jpg')


# create directories for sorting files
path = os.path.join(folder, '_Graphics')
if not os.path.exists(path):
	os.mkdir(path)
path = os.path.join(folder, '_Maybe')
if not os.path.exists(path):
	os.mkdir(path)


# run all images
graphics_count = 0
maybe_count = 	 0
photo_count = 	 0
for i, image in enumerate(images):
	print str(i+1) + '/' + str(len(images)) + ': ' + os.path.basename(image)
	
	# get image entropy
	# lower entropy usually == graphics
	px = os.popen('convert -format "%w*%h\n" "' + image + '" info:|bc').read().strip()
	cmd = 'convert "' + image + '" -colorspace gray -depth 8 -format "%c" histogram:info:- | awk -F: -v px=' + px + ' \'{p=$1/' + px + ';e+=-p*log(p)} END {print e}\''
	entropy = float(os.popen(cmd).read().strip())
	
	# if entropy low enough, just move to graphics
	if entropy < graphics_theshold:
		src = image
		dst = os.path.join(folder, '_Graphics', os.path.basename(image))
		shutil.move(src, dst)
		graphics_count += 1

	# not sure?
	elif entropy >= graphics_theshold and entropy < photo_threshold:
		src = image
		dst = os.path.join(folder, '_Maybe', os.path.basename(image))
		shutil.move(src, dst)
		maybe_count += 1
	
	# otherwise, consider it a photo
	else:
		photo_count += 1


# results
print '\n\n' + 'FOUND'
print ('=' * 17)
print str(graphics_count) + '\t graphics'
print str(maybe_count) + '\t maybe images'
print str(photo_count) + '\t photographs'
print '\n'

