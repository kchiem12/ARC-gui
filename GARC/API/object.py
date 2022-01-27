import numpy as np
from API.color import *
from API.util import *

"""
Object function always takes a parameter `c`, specifying the color of this object.
If c is not given (None), objects is assigned a random non-black color.
"""

def line(x = 1, y = 1, c = None):
	"""
	Draws a vertical, parallel, or diagonal line of color `c`
	Case `x`==1: Draws a vertical line of length `y`
	Case `y`==1: Draws a parallel line of length `x`
	Case `x`==y: Draws the diagonal of a square of `x`, from left-bottom to right-above
	"""
	if c == None: c = rand_color()

	if x == 1 or y == 1: return np.full((x,y), c, dtype=int)
	if x == 0 or y == 0: return np.full((1,1), Color.Black, dtype=int) # Black means nothing
	elif x == y:
		arr = np.zeros((x, y), dtype=int)
		for i in range(x):
			arr[i][i] = c
		return arr
	else: raise "Line: can only draw parallel, vertical, or diagonal"

def rectangle(x = 1, y = 1, c = None):
	"""
	Draws a filled rectangle
	"""
	if c == None: c = rand_color()
	return np.full((x,y), c, dtype=int)

def random_object(x = 1, y = 1, c = None, p = None):
	"""
	Draws a random object inside the rectangle `x` times `y`
	"""
	p = random.random() if p == None else p
	arr = np.zeros((x, y), dtype=int)
	if c == None: c = rand_color()

	for i in range(x):
		for j in range(y):
			if rand_bool(p): arr[i][j] = c
	
	return arr

def vertical_line(l, c = None):
	return line(1, l, c)

def parallel_line(l, c = None):
	return line(l, 1, c)

def diagonal_line(l, c = None):
	return line(l, l, c)

def square(l, c = None):
	return rectangle(l, l, c)