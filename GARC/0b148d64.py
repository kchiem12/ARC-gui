from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	canvas_length_range = closed_interval(15, 23)
	x_len = rand_sample(1, canvas_length_range)
	y_len = rand_sample(1, canvas_length_range)
	input_canvas = new_canvas(x_len, y_len)

	seperator_length_range = closed_interval(1, 5)
	x_sep_len = rand_sample(1, seperator_length_range)
	y_sep_len = rand_sample(1, seperator_length_range)

	# On the x-axis, we see 2 objects, get their x-length
	o1_xlen = rand_sample(1, x_len - x_sep_len - 1) + 1
	o2_xlen = x_len - x_sep_len - o1_xlen

	# On the y-axis, we see 2 objects, get their y-length
	o1_ylen = rand_sample(1, y_len - y_sep_len - 1) + 1
	o2_ylen = y_len - y_sep_len - o1_ylen

	# Among the 4 objects, 1 of them is the special object of different color 
	color_choices = rand_sample(2, non_black_colors)
	c1 = color_choices[0]
	c2 = color_choices[1]
	special_object_index = rand_sample(1, 4)
	def pick_color(i): return c2 if i == special_object_index else c1

	object_list = [[random_object(o1_xlen, o1_ylen, pick_color(0), 0.8), 0, 0],
				[random_object(o2_xlen, o1_ylen, pick_color(1), 0.8), o1_xlen+x_sep_len, 0],
				[random_object(o1_xlen, o2_ylen, pick_color(2), 0.8), 0, o1_ylen+y_sep_len],
				[random_object(o2_xlen, o2_ylen, pick_color(3), 0.8), o1_xlen+x_sep_len, o1_ylen+y_sep_len]]


	input_canvas = paint_objects(input_canvas, object_list)
	print("----input----")
	display(input_canvas)

	output_canvas = to_canvas(object_list[special_object_index][0])
	print("----output----")
	display(output_canvas)



def get_input_canvas():
	if input_canvas is None: raise CanvasNotInitiated()
	return input_canvas

def get_output_canvas():
	if output_canvas is None: raise CanvasNotInitiated()
	return output_canvas

if __name__ == "__main__":
	generate_problem()
	
