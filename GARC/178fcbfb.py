from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	
	x_len = rand_sample(1, closed_interval(8, 12))
	y_len = rand_sample(1, closed_interval(8, 12))

	# Didn't use rand_position because we had to ensure the uniqueness of each row/column
	point_number = rand_sample(1, closed_interval(3, 6))
	xs = rand_sample(point_number, x_len)
	ys = rand_sample(point_number, y_len)

	# To be consistent with later drawing output, instead of `paint_points`,
	# we use `paint_objects` here
	def gen_input_obj(x, y, c):
		return (point(c), x, y)

	input_canvas = new_canvas(x_len, y_len)
	base_red_point = (gen_input_obj(xs[0], ys[0], Color.Red))
	base_green_point = (gen_input_obj(xs[1], ys[1], Color.Green))
	base_cobalt_point = (gen_input_obj(xs[2], ys[2], Color.Cobalt))
	print("Base Points are ", list(zip(xs[:3], ys[:3], [Color.Red, Color.Green, Color.Cobalt])))

	remaining_point_number = point_number - 3
	color_pool = [Color.Red, Color.Green, Color.Cobalt]
	color_choices = rand_sample(remaining_point_number, color_pool, True)

	def is_red(c): return c == Color.Red


	remaining_xs = xs[3:]
	remaining_ys = ys[3:]
	remaining_points = list(zip(remaining_xs, remaining_ys, color_choices))
	remaining_input_points = list(map(lambda x : gen_input_obj(x[0], x[1], x[2]), 
							remaining_points))
	print("Remaining Random Points are ", remaining_points)

	input_canvas = paint_objects(input_canvas, [base_red_point, base_green_point, base_cobalt_point])
	input_canvas = paint_objects(input_canvas, remaining_input_points)

	print("----input----")
	display(input_canvas)


	output_canvas = new_canvas(x_len, y_len)
	base_red_line = (vertical_ray(Color.Red), xs[0], 0)
	base_green_line = (parallel_ray(Color.Green), 0, ys[1])
	base_cobalt_line = (parallel_ray(Color.Cobalt), 0, ys[2])

	def gen_output_obj(x, y, c):
		if c == Color.Red:
			return (vertical_ray(c), x, 0)
		else:
			return (parallel_ray(c), 0, y)

	remaining_red_outputs = list(filter(lambda x: is_red(x[2]), remaining_points))
	remaining_nonred_outputs = list(filter(lambda x: not is_red(x[2]), remaining_points))
	remaining_red_objects = list(map(lambda x : gen_output_obj(x[0], x[1], x[2]), remaining_red_outputs))
	remaining_nonred_objects = list(map(lambda x : gen_output_obj(x[0], x[1], x[2]), remaining_nonred_outputs))

	output_canvas = paint_objects(output_canvas, [base_red_line])
	output_canvas = paint_objects(output_canvas, remaining_red_objects)
	output_canvas = paint_objects(output_canvas, [base_green_line, base_cobalt_line])
	output_canvas = paint_objects(output_canvas, remaining_nonred_objects)

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
	
