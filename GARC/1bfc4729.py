from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	color_choices = rand_sample(2, non_black_colors)
	c1 = color_choices[0]
	c2 = color_choices[1]

	input_canvas = new_canvas(10, 10)
	x1 = rand_sample(1, 10)
	x2 = rand_sample(1, 10)
	input_canvas = paint_objects(input_canvas, [(point(c1), x1, 7), (point(c2), x2, 2)])
	print("----input----")
	display(input_canvas)

	output_canvas = new_canvas(10, 10)
	output_canvas = paint_objects(output_canvas, [[parallel_ray(c1), 0, 9],
												  [parallel_ray(c1), 0, 7],
												  [vertical_line(5, c1), 0, 5],
												  [vertical_line(5, c1), 9, 5]])
	output_canvas = paint_objects(output_canvas, [[parallel_ray(c2), 0, 2],
												  [parallel_ray(c2), 0, 0],
												  [vertical_line(5, c2), 0, 0],
												  [vertical_line(5, c2), 9, 0]])												  
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
	
