from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	color_choice = rand_sample(3, non_black_colors)
	print("color choices are ", color_choice)
	c1 = color_choice[0]
	c2 = color_choice[1]
	c3 = color_choice[2]

	output_canvas = new_canvas(7, 7)
	output_canvas = paint_objects(output_canvas,
								[[diagonal_ray(c1), 0, 6], 
								[diagonal_ray(c2), 0, 5],
								[diagonal_ray(c3), 0, 4],
								[diagonal_ray(c1), 0, 3],
								[diagonal_ray(c2), 0, 2],
								[diagonal_ray(c3), 0, 1],
								[diagonal_ray(c1), 0, 0],
								[diagonal_ray(c2), 1, 0],
								[diagonal_ray(c3), 2, 0],
								[diagonal_ray(c1), 3, 0],
								[diagonal_ray(c2), 4, 0],
								[diagonal_ray(c3), 5, 0],
								[diagonal_ray(c1), 6, 0]])

	# helper function to generate the inputs
	def get_x(x): return 0 if x <= 6 else x-6
	def get_y(y): return 6-y if y <= 6 else 0
	def get_color(l):
		remainder = l % 3
		if remainder == 0: return c1
		elif remainder == 1: return c2
		else: return c3

	# There are a toal 13 diagonal lines, order them from 
	# the upper left - origin - lower right
	# Among these diagonal lines, we must randomly select 3, each with a different 
	# color. These 3 lines will be shown as input
	p1 = 0 + rand_division(1, 1, 5)[0] * 3
	p2 = 1 + rand_division(1, 1, 4)[0] * 3
	p3 = 2 + rand_division(1, 1, 4)[0] * 3
	print("position choices are ", [p1, p2 ,p3])
	input_canvas = new_canvas(7, 7)
	input_canvas = paint_objects(input_canvas,
								[[diagonal_ray(get_color(p1)), get_x(p1), get_y(p1)], 
								[diagonal_ray(get_color(p2)), get_x(p2), get_y(p2)], 
								[diagonal_ray(get_color(p3)), get_x(p3), get_y(p3)]])

	print("----input----")
	display(input_canvas)
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
	
