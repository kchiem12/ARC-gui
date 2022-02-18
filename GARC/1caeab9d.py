from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	canvas_xlen = 10
	canvas_ylen = 10 if rand_bool(.5) else 5
	object_xlen = rand_sample(1, 3) + 1
	object_ylen = rand_sample(1, 3) + 1
	blue_object_index = rand_sample(1, 3)
	other_object_indexes = rand_sample(2, list(filter(lambda i : i != blue_object_index, closed_interval(0, 2))))
	print(blue_object_index, other_object_indexes)

	xs = rand_division(1, 3, canvas_xlen - object_xlen, min_dis=object_xlen)
	ys = rand_sample(3, canvas_ylen - object_ylen)

	print(xs, ys)

	
	object_points = rand_position(object_xlen, object_ylen, .75)
	o1 = paint_points(new_canvas(object_xlen, object_ylen), object_points, Color.Cobalt)
	o2 = paint_points(new_canvas(object_xlen, object_ylen), object_points, Color.Red)
	o3 = paint_points(new_canvas(object_xlen, object_ylen), object_points, Color.Yellow)

	input_canvas = new_canvas(canvas_xlen, canvas_ylen)
	input_canvas = paint_canvas(input_canvas, [[o1, xs[blue_object_index], ys[blue_object_index]],
											   [o2, xs[other_object_indexes[0]], ys[other_object_indexes[0]]],
											   [o3, xs[other_object_indexes[1]], ys[other_object_indexes[1]]]])

	print("----input----")
	display(input_canvas)

	output_canvas = new_canvas(canvas_xlen, canvas_ylen)
	output_canvas = paint_canvas(output_canvas, [[o1, xs[blue_object_index], ys[blue_object_index]],
											     [o2, xs[other_object_indexes[0]], ys[blue_object_index]],
											     [o3, xs[other_object_indexes[1]], ys[blue_object_index]]])
	print("----output----")
	display(output_canvas)
	return

def get_input_canvas():
	if input_canvas is None: raise CanvasNotInitiated()
	return input_canvas

def get_output_canvas():
	if output_canvas is None: raise CanvasNotInitiated()
	return output_canvas

if __name__ == "__main__":
	generate_problem()
	
