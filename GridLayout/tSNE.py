
'''
FINAL REDUCTION WITH TSNE
Jeff Thompson | 2017 | jeffreythompson.org

Run a final dimensionality reduction using t-SNE, which generally gives better
results than PCA. Large datasets may cause memory errors, though, so this tends
to be mostly trial-and-error.

Generally, the scikit-learn docs say that the settings don't make a ton of
difference, though you may find tweaking them does make an impact depending on
your input data.

More on the settings here:
+ http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
+ http://scikit-learn.org/stable/modules/manifold.html#t-sne

'''

import numpy as np 
from sklearn.manifold import TSNE
import h5py
import os, sys


dims = 			  2		  # how many dimensions for final reduction

learning_rate =   300     # 100-1000 usually good, shouldn't be higher (default = 1000)
						  # probably the most critical value to tune

perplexity = 	  30      # num of clusters t-SNE will try to fit to (default = 30)
						  # (larger datasets tend to require higher perplexity)

angle = 		  0.2     # 0-1 (default = 0.5)
						  # lower = more accurate fitting, higher = faster processing 

# see note above on setting these values

hdf5_filename =   'data/pca_15dims.h5'						# file to read from
output_filename = 'data/tsne_' + str(dims) + 'dims.h5'		# hdf5 file to write to


# oh hey
term_width, term_cols = os.popen('stty size', 'r').read().split()
term_width = int(term_width)
print 'FINAL REDUCTION WITH TSNE'


# load features from hdf5 file
# note that, unlike our PCA version, we load the whole
# thing into RAM here
print 'loading features from file...'
f = h5py.File(hdf5_filename)
features = f['data'][:]
print '- loaded ' + str(features.shape[0]) + ' images with ' + str(features.shape[1]) + ' features each'


# fancy progress printing
def fancy_progress(i, n):
	info = '- chunk: ' + str(i+1) + '/' + str(n)
	info += (' ' * (term_width-len(info)))
	sys.stdout.write('\r' + info)
	sys.stdout.flush()


# run reduction
print 'reducing with t-SNE...'
tsne = TSNE(n_components=dims, learning_rate=learning_rate, perplexity=perplexity, angle=angle, verbose=1).fit_transform(features)
print '- done'


# save filenames and t-SNE features to hdf5 file
print 'saving filenames...'
o = h5py.File(output_filename, 'w')
o.create_dataset('labels', data=f['labels'], compression='gzip')
print '- done'

print 'saving t-SNE features...'
o.create_dataset('data', data=pca_features, compression='gzip')
print '- done'


# all done, close both hdf5 files
o.close()
f.close()
print '\n' + 'ALL DONE!' + '\n\n'

 