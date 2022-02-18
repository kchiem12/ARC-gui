from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():
	"""
	Divides the canvas into two halves, where all the green points
	on one half are colored the same, while the other half are all colored
	in a different color.

	"""
	global input_canvas, output_canvas

	dir_canvas = rand_bool(0.2) #determines if the color wall is on the sides or top and bottom of canvas
	#if True, the color walls are placed on the sides, otherwise placed on top and bottom of canvas

	color_one = rand_color()
	color_two = rand_color()


	input_canvas = new_canvas(10, 10)
	output_canvas = new_canvas(10, 10)

	#Generates the positions of the two points depending on where the color walls are located
	#To more easily determine which points are on which half, the list of points are divided into two
	if dir_canvas: 
		points_halfone = rand_position(5, 10)
		points_halftwo = list(map(lambda x : (x[0]+5, x[1]), rand_position(5, 10)))
	else: 
		points_halfone = rand_position(10, 5)
		points_halftwo = list(map(lambda x : (x[0], x[1]+5), rand_position(10, 5)))


	input_canvas = paint_points(input_canvas, points_halfone, 3)
	input_canvas = paint_points(input_canvas, points_halftwo, 3)


	if dir_canvas:
		colorwall_one = vertical_line(10, color_one)
		colorwall_two = vertical_line(10, color_two)
		input_canvas = paint_objects(input_canvas, [(colorwall_one, 0, 0, 0)])
		input_canvas = paint_objects(input_canvas, [(colorwall_two, 9, 0, 0)])
		output_canvas = paint_points(input_canvas, points_halfone, color_one)
		output_canvas = paint_points(output_canvas, points_halftwo, color_two)
	else:
		colorwall_one = parallel_line(10, color_one)
		colorwall_two = parallel_line(10, color_two)
		input_canvas = paint_objects(input_canvas, [(colorwall_one, 0, 0, 0)])
		input_canvas = paint_objects(input_canvas, [(colorwall_two, 0, 9, 0)])
		output_canvas = paint_points(input_canvas, points_halfone, color_one)
		output_canvas = paint_points(output_canvas, points_halftwo, color_two)


	print("----input----")
	display(input_canvas)
	print("\n----output----")
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
	
