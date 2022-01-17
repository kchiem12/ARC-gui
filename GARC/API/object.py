import numpy as np
from API.color import *
from API.util import *

def line(x = 1, y = 1, c = None):
	if c == None: c = rand_color()

	if x == 1 or y == 1: return np.full((x,y), c, dtype=int)
	elif x == y:
		arr = np.zeros((x, y), dtype=int)
		for i in range(x):
			arr[i][i] = c
		return arr
	else: raise "Line: can only draw parallel, vertical, or diagonal"

def rectangle(x = 1, y = 1, c = None):
	if c == None: c = rand_color()
	return np.full((x,y), c, dtype=int)

def random_object(x = 1, y = 1, c = None):
	arr = np.zeros((x, y), dtype=int)
	if c == None: c = rand_color()

	for i in range(x):
		for j in range(y):
			if rand_bool(): arr[i][j] = c
	
	return arr

def vertical_line(l, c = None):
	return line(1, l, c)

def parallel_line(l, c = None):
	return line(l, 1, c)

def diagonal_line(l, c = None):
	return line(l, l, c)

def square(l, c = None):
	return rectangle(l, l, c)