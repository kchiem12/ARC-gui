from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	'''
	Symmetry Task

	input is a 3x3 grid with colored tiles randomly dispersed

	output is a 3x6 grid, where the input grid is mirrored along the center y-axis
	'''

	#random color
	color = rand_color()

	#generating the input
	input_canvas = new_canvas(3, 3)
	in_position = rand_position(input_canvas)
	input_canvas = paint_points(input_canvas, in_position, color)
	print("----input----")
	display(input_canvas)


	#generating the output
	output_canvas = new_canvas(6, 3)
	rotated_in = flip_x(input_canvas)
	output_canvas = paint_points(output_canvas, in_position, color)
	obj_list = [(rotated_in, 3, 0, 0)] #for the parameter of creating the object on canvas
	output_canvas = paint_objects(output_canvas, obj_list)
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
	print(input_canvas)
