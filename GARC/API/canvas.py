import numpy as np
import random
from API.color import *
from API.util import *
from API.exception import *

dir_map = [[1,1], [1,-1], [-1,-1], [-1,1]]

"""
Canvas is a numpy array specifying what color each position has
canvas[x][y] = color
"""

def new_canvas(x, y):
	"""
	Returns a canvas with x-axis of length `x` and y-axis of length `y`
	"""
	return np.zeros((x, y),dtype=int)

def x_length(canvas):
	"""
	Returns the length of this canvas along x-axis
	"""
	return len(canvas)

def y_length(canvas):
	"""
	Returns the length of this canvas along y-axis
	"""
	return len(canvas[0])

def paint_objects(canvas, objs_to_draw):
	"""
	Returns a new canvas with objects specified by `objs_to_draw` painted on `canvas`
	Caution: The use of dir parameter should be very limited

	Parameters
	----------
	canvas : numpy.array
		Original canvas to draw the objects on
	objs_to_draw : list
		A list containing a description for each object to draw,
		such description is in the format [obj, x, y, dir]:
			obj (Object): An object to be drawn
			x, y (int): the x and y coordinates starting from which we draw this object `obj`
			dir (int): the quadrant in which we will draw the object `obj`, optional and default 0
		To draw the `obj` according to `x`, `y`, `dir`, we first draw a coordinate
		system at point (`x`, `y`) on `canvas` and draw `obj` on the `dir` 
		quadrant of this coordinate system. 
	"""
	canvas = np.array(canvas)
	for i in range(len(objs_to_draw)):
		# print("Drawing the %dth object" %(i))
		obj_to_draw = objs_to_draw[i]
		obj = obj_to_draw[0]
		x1 = obj_to_draw[1]
		y1 = obj_to_draw[2]
		if len(obj_to_draw) > 3: raise "Not Implemented"

		for j in range(x_length(canvas)):
			for k in range(y_length(canvas)):
				color_to_paint = obj.fun(j - x1, k - y1)
				if color_to_paint != Color.Black: canvas[j][k] = color_to_paint
	
	return canvas

def paint_canvas(canvas, canvases_to_draw):
	"""
	Returns a new canvas with canvases specified by `canvases_to_draw` painted on `canvas`
	
	Parameters
	----------
	canvas : numpy.array
		Original canvas to draw the objects on
	canvases_to_draw : list
		A list containing a description for each canvas to draw,
		such description is in the format [c, x, y, dir]:
			c (numpy.array): A canvas to be drawn
			x, y (int): the x and y coordinates starting from which we draw this canvas `c`
			dir (int): the quadrant in which we will draw the canvas `c`, optional and default 0
		To draw the `c` according to `x`, `y`, `dir`, we first draw a coordinate
		system at point (`x`, `y`) on `canvas` and draw `c` on the `dir` 
		quadrant of this coordinate system. 
	"""
	canvas = np.array(canvas)
	for i in range(len(canvases_to_draw)):
		# print("Drawing the %dth object" %(i))
		canvas_to_draw = canvases_to_draw[i]
		obj = canvas_to_draw[0]
		x1 = canvas_to_draw[1]
		y1 = canvas_to_draw[2]
		dir = canvas_to_draw[3] % 4 if len(canvas_to_draw) > 3 else 0

		if not (x_length(obj) == 1 or y_length(obj) == 1):
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
				canvas[i + xs][j + ys] = obj[i][j] if obj[i][j] != Color.Black else canvas[i + xs][j + ys]
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
	canvas = np.array(canvas)
	color = rand_color() if color == None else color
	for (i, j) in points:
		canvas[i][j] = color
	return canvas

def to_canvas(obj):
	"""
	Returns `obj` on a fit canvas
	"""
	return obj.arr

def display(canvas):
	"""
	Prints `canvas` in ASCII format
	"""
	max_y = len(canvas[0])
	for j in range(max_y):
		for i in range(len(canvas)):
			print(canvas[i][max_y - j - 1], end= " ")
		print()