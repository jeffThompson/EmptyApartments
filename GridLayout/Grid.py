
'''
GRID LAYOUT
Jeff Thompson | 2017 | jeffreythompson.org

Converts the cloud of 2D data from t-SNE into a nice grid using
Rasterfairy.

'''

import rasterfairy
# import GridOptimizer
import numpy as np

grid_width =           315		# how many images across? (essentially sqrt(num_images))
grid_height =          395		# ditto height
cut_off_at_grid_size = True		# cut off when we've reached an even grid (specified above)?
								# if false, will default to the auto-layout from RasterFairy
force_layout =         False	# force RasterFairy to use grid_width and height

perplexity = 	       30		# for loading and saving filename

num_iterations =       1		# for optimzed layout at bottom

input_filename = 'data/MulticoreTSNE_2dims_' + str(perplexity) + 'perplexity.csv'
output_filename = 'data/Grid_' + str(perplexity) + 'perplexity.csv'


# load up all 2D points and filenames
print 'loading data from file...'
filenames = []
X = []
with open(input_filename) as f:
	f.next()						# skip header
	for i, line in enumerate(f):
		if cut_off_at_grid_size and i > grid_width * grid_height:
			break
		line = line.strip().split(',')
		filenames.append(line[0])
		X.append( [ float(line[1]), float(line[2]) ] )
X = np.array(X)
num_datapoints = len(filenames)
print '- loaded data for ' + str(num_datapoints) + ' images'


# calculate arrangement
print 'calculating arrangements...'
arrangements = rasterfairy.getRectArrangements(num_datapoints)
print '- best candidate: ' + str(arrangements[0])
if force_layout:
	print '- ignoring and using (' + str(grid_width) + 'x' + str(grid_height) + ') instead'


# convert to a grid, save results to a CSV file for later use
print 'laying out grid...'
if force_layout:
	grid, (width, height) = rasterfairy.transformPointCloud2D(X, target=(grid_width, grid_height))
else:
	grid, (width, height) = rasterfairy.transformPointCloud2D(X, target=arrangements[0])
data = zip(filenames, grid)
with open(output_filename, 'w') as f:
	f.write('path,x,y' + '\n')
	for path, pos in data:
		f.write(path + ',' + str(int(pos[0])) + ',' + str(int(pos[1])) + '\n')
print '- done (laid out to ' + str(width) + 'x' + str(height) + ' grid)'


# try optimizing the grid layout, though may choke on large data # print 'optimizing (' + str(num_iterations) + ' iterations)'
# optimizer = rfoptimizer.SwapOptimizer()
# swap_table = optimizer.optimize(X, grid, grid_width, grid_height, num_iterations)


print '\n' + 'ALL DONE!'

