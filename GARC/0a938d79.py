from API.canvas import *
from API.object import *
from API.color import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	l = rand_sample(1, closed_interval(16, 30))
	w = rand_sample(1, closed_interval(6, 10))

	output_canvas = new_canvas(l, w)
	starting_positions = rand_division(1, 2, int(l / 2))
	s1 = starting_positions[0]
	s2 = starting_positions[1]
	color_choices = rand_sample(2, non_black_colors)
	c1 = color_choices[0]
	c2 = color_choices[1]

	print("starting from ", starting_positions)

	dis = 2 * (s2 - s1)

	positions1 = list(map(lambda x : x*dis + s1, closed_interval(0, l)))
	p1_within_canvas = list(filter(lambda x : x<l, positions1))
	positions2 = list(map(lambda x : x*dis + s2, closed_interval(0, l)))
	p2_within_canvas = list(filter(lambda x : x<l, positions2))

	o1 = vertical_line(y_length(output_canvas), c1)
	o2 = vertical_line(y_length(output_canvas), c2)
	for p1 in p1_within_canvas:
		output_canvas = paint_objects(output_canvas, [[o1, p1, 0, 0]])
	for p2 in p2_within_canvas:
		output_canvas = paint_objects(output_canvas, [[o2, p2, 0, 0]])

	input_canvas = new_canvas(l, w)
	input_canvas = paint_points(input_canvas, [(s1, w-1)], c1)
	input_canvas = paint_points(input_canvas, [(s2, 0)], c2)

	vertical = rand_bool()
	if vertical:
		input_canvas = rotate_90(flip_y(input_canvas))
		# input_canvas = rotate_90(input_canvas)
		output_canvas = rotate_90(output_canvas)

	print("----input----")
	display(input_canvas)
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
	