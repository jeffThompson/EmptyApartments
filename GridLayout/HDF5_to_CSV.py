
'''
HDF5 TO CSV
Jeff Thompson | 2017 | jeffreythompson.org

Converts an HDF5 file to CSV - needed for gridding with Rasterfairy,
but also easier for parsing with Processing or creating human-readable files.

Optionally, normalize the data too while we're at it...
** NOTE: we do NOT want to normalize if we're using RasterFairy - seems to break it.

'''

import h5py

normalize = 	  False		# normalize data 0-1?
dims = 			  2			# how many dimensions to this data?
perplexity =      30		# what was the perplexity?

hdf5_filename = 'data/MulticoreTSNE_' + str(dims) + 'dims_' + str(perplexity) + 'perplexity.h5'
output_filename = 'data/MulticoreTSNE_' + str(dims) + 'dims_' + str(perplexity) + 'perplexity.csv'


# normalize value 0-1
def norm(i, min_val, max_val):
	return (i-min_val) / (max_val-min_val)


# load features from hdf5 file
# note that, unlike our PCA version, we load the whole
# thing into RAM here
print 'loading features from file...'
f = h5py.File(hdf5_filename)
features = f['data'][:]
print '- loaded ' + str(features.shape[0]) + ' images with ' + str(features.shape[1]) + ' features each'


# get min/max values from data
if normalize:
	print 'finding min/max values...'
	min_x, min_y = features.min(axis=0)
	max_x, max_y = features.max(axis=0)
	print '- min: ' + str(min_x) + ', ' + str(min_y)
	print '- max: ' + str(max_x) + ', ' + str(max_y)


# save filenames and t-SNE features to hdf5 file
if normalize:
	print 'saving normalized data (may take a bit)...'
	output_filename = output_filename.replace('.csv', '-NORMALIZED.csv')
else:
	print 'saving data...'
with open(output_filename, 'w') as out:
	out.write('path,x,y' + '\n')
	for path, data in zip(f['labels'], features):
		path = path.replace('/Combo/', '/NotBlurred/')
		x = data[0]
		y = data[1]
		if normalize:
			x = norm(x, min_x, max_x)
			y = norm(y, min_y, max_y)
		out.write(path + ',' + str(x) + ',' + str(y) + '\n')
print '- done'

