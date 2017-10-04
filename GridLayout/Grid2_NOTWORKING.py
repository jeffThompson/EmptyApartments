
'''
GRID LAYOUT
Jeff Thompson | 2017 | jeffreythompson.org

Converts the cloud of 2D data from t-SNE into a nice grid using
Rasterfairy.

'''

import rasterfairy
from GridOptimizer import *
import numpy as np

grid_width =       363			# how many images across? (essentially sqrt(num_images))
grid_height =      362			# ditto height
perplexity = 	   30
num_iterations =   1000		# for optimzed layout (10k at least, more most likely needed)
shake_iterations = 5

input_filename = 'data/MulticoreTSNE_2dims_' + str(perplexity) + 'perplexity.csv'
output_filename = 'data/Grid_' + str(perplexity) + 'perplexity-OPTIMIZED.csv'


# get min/max positions for x/y
print 'getting min/max positions...'
min_x = max_x = min_y = max_y = 0
with open(input_filename) as f:
	f.next()						# skip header
	for line in f:
		line = line.strip().split(',')
		x = float(line[1])
		y = float(line[2])
		if x < min_x:
			min_x = x
		elif x > max_x:
			max_x = x
		if y < min_y:
			min_y = y
		elif y > max_y:
			max_y = y
data_width = max_x - min_x
data_height = max_y - min_y
print '- extents:'
print '  X: ' + str(min_x) + ' to ' + str(max_x) + ' (' + str(data_width) + ' wide)'
print '  Y: ' + str(min_y) + ' to ' + str(max_y) + ' (' + str(data_height) + ' high)'


def run(start_x, end_x, start_y, end_y):
	print '(' + str(start_x) + ', ' + str(start_y) + ')'
	
	# load up all 2D points and filenames
	print 'loading data from file...'
	filenames = []
	X = []
	with open(input_filename) as f:
		f.next()						# skip header
		for i, line in enumerate(f):
			line = line.strip().split(',')
			x = float(line[1])
			y = float(line[2])
			if x >= start_x and x <=end_x and y >= start_y and y <= end_y:
				X.append( [ x, y ] )
				filenames.append(line[0])

	X = np.array(X)
	num_datapoints = X.shape[0]
	print '- loaded data for ' + str(num_datapoints) + ' images'


	# calculate arrangement
	print 'calculating arrangements...'
	arrangements = rasterfairy.getRectArrangements(num_datapoints)
	print '- best candidate: ' + str(arrangements[0])


	# convert to a grid
	print 'laying out grid...'
	# grid, (width, height) = rasterfairy.transformPointCloud2D(X, target=(grid_width,grid_height))
	grid, (width, height) = rasterfairy.transformPointCloud2D(X, target=arrangements[0])
	print '- done (laid out to ' + str(width) + 'x' + str(height) + ' grid)'


	# try optimizing the grid layout, though may choke on large data 
	print 'optimizing (' + str(num_iterations) + ' iterations)'
	optimizer = SwapOptimizer()
	swap_table, improvement = optimizer.optimize(X, grid, width, height, num_iterations, verbose=False)
	print '- improvement of ' + str(improvement)
	if improvement > 0:
		print 'still room for more optimization, running again...'
		iterations = 0
		num_improvement_iterations = 5
		while True:
			if improvement <= 0:
				print '  - no more improvement, stopping...'
				break
			elif iterations == num_improvement_iterations:
				print '  - reached max number of iterations, stopping...'
				break
			
			print '- continuing ' + str(num_iterations) + ' iterations of optimization...'
			swap_table, improvement = optimizer.continueOptimization(iterations*num_iterations, shakeIterations=shake_iterations, verbose=False)
			iterations += 1
			print '  - improvement of ' + str(improvement)
	print '- done'


	# save results to a csv file for later use
	print 'saving to file...'
	data = zip(filenames, grid[swap_table])
	with open(output_filename, 'w') as f:
		f.write('path,x,y' + '\n')
		for path, pos in data:
			f.write(path + ',' + str(int(pos[0])) + ',' + str(int(pos[1])) + '\n')
	print '- done'


# divide data into regions and run gridding
print ''
num_divisions = 3
for y in range(num_divisions):
	for x in range(num_divisions):
		print str(x) + '/' + str(y) + '...'
		start_x = min_x + (x*data_width/num_divisions)
		end_x = start_x + (data_width/num_divisions)
		start_y = min_y + (y*data_height/num_divisions)
		end_y = start_y + (data_height/num_divisions)
		run(start_x, end_x, start_y, end_y)
		print ''
		break
print 'ALL DONE!'		
