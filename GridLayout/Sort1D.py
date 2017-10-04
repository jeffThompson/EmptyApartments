
'''
SORT 1D
Jeff Thompson | 2017 | jeffreythompson.org

Takes a CSV file of filenames and 2D positions and returns
a list of original image files and their 1D position (a single
list).

'''


grid_width = 315
perplexity = 30

intput_filename = 'data/Grid_' + str(perplexity) + 'perplexity.csv'
output_filename = '../GenerateSlippyMapTiles/Grid_' + str(perplexity) + 'perplexity-SORTED.txt'


# load up the data
data = []
with open(intput_filename) as f:
	f.next()						# skip header
	for line in f:
		line = line.strip()
		line = line.split(',')
		path = line[0]
		path = path.replace('64x64/Combo-NoDupes', 'FINAL')
		pos = int(line[2]) * grid_width + int(line[1])
		line = [ path, pos ]
		data.append(line)


# sort it, save it
data = sorted(data, key=lambda x: x[1])
with open(output_filename, 'w') as f:
	for d in data:
		f.write(d[0] + '\n')
