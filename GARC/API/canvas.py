import numpy as np
import random
from API.color import *
from API.util import *

dir_map = [[1,1], [1,-1], [-1,-1], [-1,1]]

def new_canvas(x, y):
	"""
	Returns a canvas with x-axis of length `x` and y-axis of length `y`
	"""
	return np.zeros((x, y),dtype=int)

def length(canvas):
	"""
	Returns the length of this canvas along x-axis
	"""
	return len(canvas)

def width(canvas):
	"""
	Returns the length of this canvas along y-axis
	"""
	return len(canvas[0])

def paint_objects(canvas, objs_to_draw):
	"""
	Returns a new canvas with objects specified by `objs_to_draw` painted on `canvas`

	Parameters
	----------
	canvas : numpy.array
		Original canvas to draw the objects on
	objs_to_draw : list
		A list containing a description for each objects to draw:
		For each object to draw, such description is in the format [obj, x, y, dir]:
			obj (Object): An object to be drawn
			x, y (int): the x and y coordinates starting from which we draw this object `obj`
			dir (int): the quadrant in which we will draw the object `obj`
		To draw the `obj` according to `x`, `y`, `dir`, we first draw a coordinate
		system at point (`x`, `y`) on `canvas` and draw `obj` on the `dir` 
		quadrant of this coordinate system. 
	"""
	for obj_to_draw in objs_to_draw:
		obj = obj_to_draw[0]
		x1 = obj_to_draw[1]
		y1 = obj_to_draw[2]
		dir = obj_to_draw[3] % 4

		obj = rotate_90(obj, dir)
		l = len(obj)
		w = len(obj[0])
		x2 = x1 + l * dir_map[dir][0]
		y2 = y1 + w * dir_map[dir][1]

		xs = min(x1, x2)
		xe = max(x1, x2)
		ys = min(y1, y2)
		ye = max(y1, y2)
		
		for i in range(abs(xe - xs)):
			for j in range(abs(ye - ys)):
				canvas[i + xs][j + ys] = obj[i][j] if obj[i][j] != Black else canvas[i + xs][j + ys]
	return canvas

def paint_points(canvas, points, color = None):
	"""
	Paint positions given by `points` with `color`

	Parameters
	----------
	points : [(x1, y1), (x2, y2), ...]
		x, y coordinates on `canvas` to be painted
	color : Color literal, optional
		color these points should be painted with, by default None
	"""
	color = rand_color() if color == None else color
	for (i, j) in points:
		canvas[i][j] = color
	return canvas

def display(canvas):
	"""
	Prints `canvas` in ASCII format
	"""
	max_y = len(canvas[0])
	for j in range(max_y):
		for i in range(len(canvas)):
			print(canvas[i][max_y - j - 1], end= " ")
		print()


def rand_position(canvas):
	"""
	Returns a list of random (x,y) coordinates on `canvas`

	Returns
	-------
	[(x1, y1), (x2, y2), ...]
		Each (x,y) is a valid coordinate pair on `canvas`
	"""
	lst = []
	p = random.random()
	for i in range(length(canvas)):
		for j in range(width(canvas)):
			if rand_bool(p): lst.append((i, j))
	return lst

def rand_division(n = 1, m = 1, l = 1):
	"""
	Divide number `l` into 1~`n` divisions, each division contains `m` numbers

	Parameters
	----------
	n : int, optional
		Max number of division we want, final number of divisions will be drawn 
		uniformly from [1,n], by default 1
	m : int, optional
		Number of numbers in each division, by default 1
	l : int, optional
		Number to divide, by default 1

	Returns
	-------
	Case1 `n`==1 or `m`==1: [x1, x2, ...]
		A sorted list of `n` * `m` numbers randomly drawn from range `l`
	Case2 otherwise: [(x11, x12, ...), (x21, x22, ...), ... ]
		A list of n' tuples, where n' is a random number from [1, `n`]
		Each tuple represents a division. Each division has `m` numbers
		xij (i <= n', j <= m) represents the jth number in division i
		The list is sorted: x11 < x12 < ... < x21 < x22 < ...	
	"""
	flat = n == 1 or m == 1
	n = random.randint(1, n)
	print("n %d, m %d" %(n, m))
	pool = [i for i in range(l)]
	random.shuffle(pool)
	lst = sorted(pool[:n*m])
	if flat: return lst
	this_division = []
	result = []
	print(lst)
	for i in range(n*m):
		this_division.append(lst[i])
		if (i+1) % m == 0:
			result.append(this_division)
			this_division = []
	return result