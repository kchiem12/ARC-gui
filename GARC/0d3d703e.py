from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas
	colors = [1,2,3,4,5,6,8,9]

	input_colors = rand_sample(3, colors)
	input_canvas = new_canvas(3, 3)
	input_canvas = paint_objects(input_canvas, 
								[[vertical_ray(input_colors[0]), 0, 0],
								[vertical_ray(input_colors[1]), 1, 0],
								[vertical_ray(input_colors[2]), 2, 0]])
	print("----input----")
	display(input_canvas)

	def color_map(c):
		if c == 1: return 5
		elif c == 2: return 6
		elif c == 3: return 4
		elif c == 4: return 3
		elif c == 5: return 1
		elif c == 6: return 2
		elif c == 8: return 9
		elif c == 9: return 8

	output_colors = list(map(color_map, input_colors))
	output_canvas = new_canvas(3, 3)
	output_canvas = paint_objects(output_canvas, 
								[[vertical_ray(output_colors[0]), 0, 0],
								[vertical_ray(output_colors[1]), 1, 0],
								[vertical_ray(output_colors[2]), 2, 0]])

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
	
