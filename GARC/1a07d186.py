from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	x_len = rand_sample(1, closed_interval(10, 30))
	y_len = rand_sample(1, closed_interval(10, 30))

	line_positions = rand_division(3, 1, x_len, min_dis=3)
	line_number = len(line_positions)
	point_cate_number = line_number + 1
	
	color_choices = rand_sample(point_cate_number, non_black_colors)
	line_colors = color_choices[:line_number]

	point_number = rand_sample(1, closed_interval(2*point_cate_number, 4*point_cate_number))
	point_xs = rand_sample(point_number, x_len, True)
	point_ys = rand_sample(point_number, y_len, True)
	point_colors = rand_sample(point_number, color_choices, True)

	# We only paint points that do not overlap with lines
	point_xycs = zip(point_xs, point_ys, point_colors)
	point_xycs = list(filter(lambda xy: xy[0] not in line_positions, point_xycs))
	def unique_xy(lst):
		xys = []
		def unique_xy_helper(lst):
			xyc = hd(lst)
			xy = xyc[:2]
			if len(lst) > 1:
				if xy in xys: 
					print("Duplication Found and Deleted")
					return unique_xy_helper(lst[1:])
				else:
					xys.append(xy)
					return con(xyc, unique_xy_helper(lst[1:]))
			if len(lst) == 1:
				if xy in xys:
					print("Duplication Found and Deleted")
					return []
				else:
					return [xyc]
		return unique_xy_helper(lst)
	point_xycs = unique_xy(point_xycs)


	def gen_line(x, c):
		return (vertical_ray(c), x, 0)
	lines = list(map(lambda x,c : gen_line(x, c), line_positions, line_colors))

	def gen_input_point(x, y ,c):
		return (point(c), x, y)
	input_points = list(map(lambda xyc : gen_input_point(xyc[0], xyc[1], xyc[2]), point_xycs))

	input_canvas = new_canvas(x_len, y_len)
	input_canvas = paint_objects(input_canvas, lines)
	input_canvas = paint_objects(input_canvas, input_points)
	
	point_xycs = list(filter(lambda xyc : xyc[2] in line_colors, point_xycs))
	line_color_pos = list(zip(line_colors, line_positions))
	def get_position(c):
		return assoc(c, line_color_pos)
	def gen_output_point(x, y, c):
		line_position = get_position(c)
		if x == line_position: raise "WOW WTF"
		x = line_position - 1 if x < line_position else line_position + 1
		return (point(c), x, y)
	output_points = list(map(lambda xyc : gen_output_point(xyc[0], xyc[1], xyc[2]), point_xycs))
	
	output_canvas = new_canvas(x_len, y_len)
	output_canvas = paint_objects(output_canvas, lines)
	output_canvas = paint_objects(output_canvas, output_points)
	
	vertical = rand_bool()
	if vertical:
		input_canvas = rotate_90(input_canvas)
		output_canvas = rotate_90(output_canvas)
	
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
	
