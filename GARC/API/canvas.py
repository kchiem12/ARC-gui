import numpy as np
import random
from API.color import *
from API.util import *

dir_map = [[1,1], [1,-1], [-1,-1], [-1,1]]

def new_canvas(l, w):
	return np.zeros((l, w),dtype=int)

def length(canvas):
	return len(canvas)

def width(canvas):
	return len(canvas[0])

def paint_objects(canvas, objs_to_draw):
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
	color = rand_color() if color == None else color
	for (i, j) in points:
		canvas[i][j] = color
	return canvas

def display(canvas):
	max_y = len(canvas[0])
	for j in range(max_y):
		for i in range(len(canvas)):
			print(canvas[i][max_y - j - 1], end= " ")
		print()


def rand_position(canvas):
	lst = []
	p = random.random()
	for i in range(length(canvas)):
		for j in range(width(canvas)):
			if rand_bool(p): lst.append((i, j))
	return lst

def rand_division(n = 1, m = 1, l = 1):
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