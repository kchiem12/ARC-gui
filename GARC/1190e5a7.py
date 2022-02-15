from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	x_len = rand_sample(1, closed_interval(10, 25))
	y_len = rand_sample(1, closed_interval(10, 25))

	color_choices = rand_sample(2, non_black_colors)
	background_color = color_choices[0]
	line_color = color_choices[1]

	# Choose positions of the seperators from x_len-2 because seperators can only 
	# be placed in the middle, you can't place the seperators at the start or the 
	# end of the canvas. After choosing the positions as if they were in the middle,
	# move them actually to the middle by +1 to all the coordinates
	x_sep_positions = rand_division(5, 1, x_len - 2, 2)
	x_sep_positions = list(map(lambda x : x+1, x_sep_positions))
	x_sep_num = len(x_sep_positions)
	x_seperators = list(map(lambda pos : [vertical_ray(line_color), pos, 0], x_sep_positions))

	y_sep_positions = rand_division(5, 1, y_len - 2, 2)
	y_sep_positions = list(map(lambda x : x+1, y_sep_positions))
	y_sep_num = len(y_sep_positions)
	y_seperators = list(map(lambda pos : [parallel_ray(line_color), 0, pos], y_sep_positions))

	input_canvas = new_canvas(x_len, y_len)
	background = rectangle(x_len, y_len, background_color)
	input_canvas = paint_objects(input_canvas, [[background, 0, 0]])
	input_canvas = paint_objects(input_canvas, x_seperators)
	input_canvas = paint_objects(input_canvas, y_seperators)

	output_canvas = new_canvas(x_sep_num+1, y_sep_num+1)
	output_object = rectangle(x_sep_num+1, y_sep_num+1, background_color)
	output_canvas = paint_objects(output_canvas, [[output_object, 0, 0]])

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
