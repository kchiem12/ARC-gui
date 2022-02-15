import numpy as np
from API.color import *
from API.util import *
from API.exception import *

MAX_LENGTH = int(10e5)

"""
Object Constructor always takes a parameter `c`, specifying the color of this object.
If c is not given (None), objects is assigned a random non-black color.
"""


class _Object():
	"""
	`fun` is used for canvas to draw the object:
		Specifically, for each position relative to its starting point, 
		it specifies what color to draw. 
		Take a Cobalt vertical line of length 3 as an example, we should have 
		(0,0) (0,1) (0,2) to be drawn Cobalt and all the other positions be 
		drawn as Black: 
		fun(0,0) = fun(0,1) = fun(0,2) = Color.Cobalt; fun(any pair else) = Black
	`arr` is an array representation of the object, similarly to canvas:
		For the same example, arr[0][0] = arr[0][1] = arr[0][2] = Cobalt
		arr[anything][else] = Undefined
	"""
	def __init__(self):
		self.fun = None
		self.arr = None

def _fun_builder(cond, c):
	if c == None: c = rand_color()
	return lambda x, y : c if cond(x, y) else Color.Black

def _line(x = 1, y = 1, c = None):
	"""
	Legacy code to generate array representation of a vertical, parallel, or diagonal line of color `c`
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

""" Above are private codes not exposed to User
------------------------------------ 
	Below are public APIs user should use to construct an object """

def rectangle(xl = 1, yl = 1, c = None):
	"""
	Returns a rectangle of x length `xl`, y length `yl` and color `c`
	"""
	obj = _Object()
	def cond(x,y): return (x >=0 and x < xl and y >=0 and y < yl)
	obj.fun = _fun_builder(cond, c)
	
	if c == None: c = rand_color()
	obj.arr = np.full((xl,yl), c, dtype=int)
	return obj

def random_object(x = 1, y = 1, c = None, p = None):
	"""
	Returns a random object inside the rectangle `x` times `y`
	"""
	obj = _Object()

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
	obj.fun = _fun_builder(cond, c)
	obj.arr = arr
	return obj


def vertical_line(l, c = None):
	"""
	Returns a vertical line of length `l` and color `c`
	"""
	obj = _Object()
	def cond(x,y): return (x == 0 and y >=0 and y < l)
	obj.fun = _fun_builder(cond, c)
	obj.arr = _line(1, l, c)
	return obj

def parallel_line(l, c = None):
	"""
	Returns a parallel line of length `l` and color `c`
	"""
	obj = _Object()
	def cond(x,y): return (y == 0 and x >=0 and x < l)
	obj.fun = _fun_builder(cond, c)
	obj.arr = _line(l, 1, c)
	return obj

def diagonal_line(l, c = None):
	"""
	Returns a diagonal line pointing uppper-right of length `l` and color `c`
	"""	
	obj = _Object()
	def cond(x,y): return (x == y and x >=0 and x < l and y >=0 and y < l)
	obj.fun = _fun_builder(cond, c)
	obj.arr = _line(l, l, c)
	return obj

def square(l, c = None):
	"""
	Returns a square of length `l` and color `c`
	"""	
	return rectangle(l, l, c)

def vertical_ray(c = None):
	"""
	Returns a vertical ray (of infinite length) and color `c`
	"""
	obj = _Object()
	def cond(x,y): return x == 0
	obj.fun = _fun_builder(cond, c)
	return obj

def parallel_ray(c = None):
	"""
	Returns a parallel ray (of infinite length) and color `c`
	"""
	obj = _Object()
	def cond(x,y): return y == 0
	obj.fun = _fun_builder(cond, c)
	return obj

def diagonal_ray(c = None):
	"""
	Returns a diagonal ray (of infinite length) pointing uppper-right and color `c`
	"""
	obj = _Object()
	def cond(x,y): return x == y
	obj.fun = _fun_builder(cond, c)
	return obj