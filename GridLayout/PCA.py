
'''
PRELIMINARY REDUCTION WITH PCA
Jeff Thompson | 2017 | jeffreythompson.org

Runs a preliminary reduction in the number of vectors in our data
(a process called "decomposition") using Incremental Principle
Component Analysis (or Incremental PCA). This reduces the size of
our data file considerably, removes duplicate vectors, and is
necessary if we want to use t-SNE for flattening to 2D or 3D later.

Normal PCA from sklearn works great, but for big datasets that
can't be loaded into RAM all at once, we can stream from the HDF5
file and use Incremental PCA. First, we iterate our dataset and 
fit the PCA to it, then iterate again (sadly) and run the transformation.

HOW MANY DIMENSIONS?
A good question. PCA requires that the number of dimensions be no
larger than the number of elements (not the # of vectors in those
elements), but generally the issue is more about how few is ok.

Imanol Luengo suggests here (https://stackoverflow.com/a/44335148/1167783)
that a good starting point is to use the square root of the number of
vectors in one datapoint, ie sqrt(features.shape[1]).

Generally, trying to go down to 2D with PCA will not give good results.
A first-round PCA followed by t-SNE (as we do here) is the best
bet for that.

'''

import numpy as np 
from sklearn.decomposition import IncrementalPCA
import h5py
import cPickle as pickle
import os, sys


dims = 			   150				# how many dims in the final reduction?
chunk_size =       1000 		    # how many rows at a time to feed ipca

hdf5_filename =   'data/Features.h5'						# file to read from
output_filename = 'data/PCA_' + str(dims) + 'dims.h5'		# hdf5 file to write to


# oh hey
term_width, term_cols = os.popen('stty size', 'r').read().split()
term_width = int(term_width)
print 'PRELIMINARY DECOMPOSITION WITH PCA'


# load features from hdf5 file
print 'loading features from file...'
f = h5py.File(hdf5_filename)
features = f['data']
print '- loaded ' + str(features.shape[0]) + ' images with ' + str(features.shape[1]) + ' features each'


# fancy progress printing
def fancy_progress(i, n):
	info = '- chunk: ' + str(i+1) + '/' + str(n)
	info += (' ' * (term_width-len(info)))
	sys.stdout.write('\r' + info)
	sys.stdout.flush()


# use IncrementalPCA to reduce vector count before TSNE reduction
# regular PCA works great for small-ish datasets, but for big ones
# that can't all be loaded into RAM at once, IPCA lets us stream the data
print 'fitting IPCA to data...'
num_images = features.shape[0]					# how many images?
if dims > num_images:							# reduction can't be > num images
	dims = num_images
num_iterations = num_images // chunk_size		# how many chunks in the data?
ipca = IncrementalPCA(n_components=dims)
for i in range(0, num_iterations):
	fancy_progress(i, num_iterations)
	ipca.partial_fit(features[i*chunk_size : (i+1)*chunk_size])
print '\n' + '- done'


# run transformation on fitted data to reduce dimensions
print 'transforming data...'
pca_features = np.empty([num_images, dims])
for i in range(0, num_iterations):
	fancy_progress(i, num_iterations)
	start = i * chunk_size
	end =   (i+1) * chunk_size
	pca_features[start:end] = ipca.transform(features[start:end])
print '\n' + '- done'


# save filenames and decomposed features to hdf5 file
print 'saving filenames...'
o = h5py.File(output_filename, 'w')
o.create_dataset('labels', data=f['labels'], compression='gzip')
print '- done'

print 'saving decomposed features...'
o.create_dataset('data', data=pca_features, compression='gzip')
print '- done'


# all done, close up the hdf5 files
o.close()
f.close()
print '\n' + 'ALL DONE!' + '\n\n'

