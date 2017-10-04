
'''
LEAST COMMON MULTIPLE
Jeff Thompson | 2016 | jeffreythompson.org


'''

import fractions

h = 400
tile_height = 256

def lcm(a, b): return abs(a*b) / fractions.gcd(a,b) if a and b else 0

print lcm(tile_height, h), 'px'