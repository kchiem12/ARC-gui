from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas
	input_canvas = new_canvas(3, 3)
	in_pos = rand_position(input_canvas)
	color = rand_color()
	input_canvas = paint_points(input_canvas, in_pos, color)
	display(input_canvas)


	output_canvas = new_canvas(9, 9)
	out_obj = list(map(lambda x : (input_canvas, 3 * x[0], 3 * x[1], 0), in_pos))
	output_canvas = paint_objects(output_canvas, out_obj)
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
	
