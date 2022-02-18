from functools import reduce
from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	input_canvas = new_canvas(7, 5)
	left_points = rand_position(3, 5)
	right_points = rand_position(3, 5)
	left_canvas = paint_points(new_canvas(3,5), left_points, Color.Brown)
	right_canvas = paint_points(new_canvas(3,5), right_points, Color.Brown)
	input_canvas = paint_canvas(input_canvas, [[left_canvas, 0, 0], 
											   [right_canvas, 4, 0]])
	input_canvas = paint_objects(input_canvas, [[vertical_ray(Color.Cobalt), 3, 0]])
	print("----input----")
	display(input_canvas)
	
	
	output_canvas = new_canvas(3, 5)
	blank_canvas = list(reduce(lambda acc,x : acc + list(map(lambda y : (x,y), closed_interval(0, 4))), closed_interval(0, 2), []))
	not_overlapped_points = list(filter(lambda x : x not in left_points and x not in right_points, blank_canvas))
	output_canvas = paint_points(output_canvas, not_overlapped_points, Color.Sky)
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
	
