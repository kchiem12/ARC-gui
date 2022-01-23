from turtle import right
from API.canvas import *
from API.object import *
from API.color import *

input_canvas = new_canvas(7, 3)

left_object = new_canvas(3, 3)
left_points = rand_position(left_object)
left_object = paint_points(left_object, left_points, Color.Cobalt)

right_object = new_canvas(3, 3)
right_points = rand_position(right_object)
right_object = paint_points(right_object, right_points, Color.Cobalt)

input_canvas = paint_objects(input_canvas,
							 [[left_object, 0, 0, 0],
							  [vertical_line(3, Color.Gray), 3, 0, 0],
							  [right_object, 4, 0, 0]])
display(input_canvas)

output_canvas = new_canvas(3, 3)
overlapped_points = list(filter(lambda x: x in right_points, left_points))
output_canvas = paint_points(output_canvas, overlapped_points, Color.Red)
display(output_canvas)