from API.canvas import *
from API.object import *
from API.color import *

input_objects = []
output_objects = []

def gen_input_obj(lower_y, upper_y):
	color = rand_color()
	dis_y = upper_y - lower_y
	upper_x = rand_division(1, 2, x_length(input_canvas) - dis_y + 1, min_dis=2)
	print("Let's look at start and endpoint of upper parallel line")
	print(upper_x)
	upper_xs = upper_x[0]
	upper_xe = upper_x[1]
	print("upper x start %d, upper x end %d on line %d, y distance %d" %(upper_xs, upper_xe, upper_y, dis_y))
	dis_x = upper_xe - upper_xs
	lower_xs = upper_xs + (dis_y - 1)

	input_upper_line = [parallel_line(dis_x, color), upper_xs, upper_y, 0]
	input_left_line = [diagonal_line(dis_y-1, color), upper_xs, upper_y, 1]
	input_right_line = [diagonal_line(dis_y-1, color), upper_xe, upper_y, 1]
	input_lower_line = [parallel_line(dis_x, color), lower_xs, lower_y, 0]
	input_objects.append([input_upper_line, input_left_line, input_right_line, input_lower_line])

	output_upper_line = [parallel_line(dis_x, color), upper_xs+1, upper_y, 0]
	output_left_line = [diagonal_line(dis_y-1, color), upper_xs+1, upper_y, 1]
	output_right_line = [diagonal_line(dis_y-2, color), upper_xe+1, upper_y, 1]
	output_right_point = [parallel_line(1, color), lower_xs+dis_x-1, lower_y+1, 0]
	output_lower_line = [parallel_line(dis_x, color), lower_xs, lower_y, 0]
	output_objects.append([output_upper_line, output_left_line, output_right_line, output_right_point, output_lower_line])
	

input_canvas = new_canvas(10, 15)
output_canvas = new_canvas(10, 15)

l = rand_division(3, 2, 15, min_dis=2, max_dis=x_length(input_canvas))
print(l)

for i in range(len(l)):
	print("Drawing the %dth rectangle" %(i))
	gen_input_obj(l[i][0], l[i][1])
	input_canvas = paint_objects(input_canvas, input_objects[i])
	output_canvas = paint_objects(output_canvas, output_objects[i])

print("----input----")
display(input_canvas)
print("----output----")
display(output_canvas)

