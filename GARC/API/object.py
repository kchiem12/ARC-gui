import numpy as np
from API.color import *
from API.util import *
from API.exception import *

MAX_LENGTH = int(10e5)

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
	else: raise InvalidCommand("Line: can only draw parallel, vertical, or diagonal")

class Object():
	def __init__(self):
		self.fun = None
		self.arr = None

def object_builder(cond, c):
	if c == None: c = rand_color()
	return lambda x, y : c if cond(x, y) else Color.Black

def rectangle(xl = 1, yl = 1, c = None):
	"""
	Draws a filled rectangle
	"""
	obj = Object()
	def cond(x,y): return (x >=0 and x < xl and y >=0 and y < yl)
	obj.fun = object_builder(cond, c)
	
	if c == None: c = rand_color()
	obj.arr = np.full((xl,yl), c, dtype=int)
	return obj

def random_object(x = 1, y = 1, c = None, p = None):
	"""
	Draws a random object inside the rectangle `x` times `y`
	"""
	obj = Object()

	p = random.random() if p == None else p
	position_list = []
	arr = np.zeros((x, y), dtype=int)
	if c == None: c = rand_color()

	for i in range(x):
		for j in range(y):
			if rand_bool(p): 
				position_list.append((i,j))
				arr[i][j] = c
	
	def cond(x, y): return (x,y) in position_list
	obj.fun = object_builder(cond, c)
	obj.arr = arr
	return obj


def vertical_line(l, c = None):
	obj = Object()
	def cond(x,y): return (x == 0 and y >=0 and y < l)
	obj.fun = object_builder(cond, c)
	obj.arr = line(1, l, c)
	return obj

def parallel_line(l, c = None):
	obj = Object()
	def cond(x,y): return (y == 0 and x >=0 and x < l)
	obj.fun = object_builder(cond, c)
	obj.arr = line(l, 1, c)
	return obj

def diagonal_line(l, c = None):
	obj = Object()
	def cond(x,y): return (x == y and x >=0 and x < l and y >=0 and y < l)
	obj.fun = object_builder(cond, c)
	obj.arr = line(l, l, c)
	return obj

def square(l, c = None):
	return rectangle(l, l, c)

def vertical_ray(c = None):
	obj = Object()
	def cond(x,y): return x == 0
	obj.fun = object_builder(cond, c)
	return obj

def parallel_ray(c = None):
	obj = Object()
	def cond(x,y): return y == 0
	obj.fun = object_builder(cond, c)
	return obj

def diagonal_ray(c = None):
	obj = Object()
	def cond(x,y): return x == y
	obj.fun = object_builder(cond, c)
	return obj