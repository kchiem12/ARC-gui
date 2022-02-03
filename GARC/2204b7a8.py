from API.canvas import *
from API.object import *
from API.color import *

"""
Divides the canvas into two halves, where all the green points
on one half are colored the same, while the other half are all colored
in a different color.

"""

dir_canvas = rand_bool(None) #determines if the color wall is on the sides or top and bottom of canvas
#if True, the color walls are placed on the sides, otherwise placed on top and bottom of canvas

color_one = rand_color()
color_two = rand_color()


in_canvas = new_canvas(10, 10)
out_canvas = new_canvas(10, 10)

#Generates the positions of the two points depending on where the color walls are located
#To more easily determine which points are on which half, the list of points are divided into two
if dir_canvas: 
	points_halfone = rand_position(new_canvas(5, 10))
	points_halftwo = list(map(lambda x : (x[0]+5, x[1]), rand_position(new_canvas(5, 5))))
else: 
	points_halfone = rand_position(new_canvas(10, 5))
	points_halftwo = list(map(lambda x : (x[0], x[1]+5), rand_position(new_canvas(5, 5))))


in_canvas = paint_points(in_canvas, points_halfone, 3)
in_canvas = paint_points(in_canvas, points_halftwo, 3)


if dir_canvas:
	colorwall_one = vertical_line(10, color_one)
	colorwall_two = vertical_line(10, color_two)
	in_canvas = paint_objects(in_canvas, [(colorwall_one, 0, 0, 0)])
	in_canvas = paint_objects(in_canvas, [(colorwall_two, 9, 0, 0)])
	out_canvas = paint_points(in_canvas, points_halfone, color_one)
	out_canvas = paint_points(out_canvas, points_halftwo, color_two)
else:
	colorwall_one = parallel_line(10, color_one)
	colorwall_two = parallel_line(10, color_two)
	in_canvas = paint_objects(in_canvas, [(colorwall_one, 0, 0, 0)])
	in_canvas = paint_objects(in_canvas, [(colorwall_two, 0, 9, 0)])
	out_canvas = paint_points(in_canvas, points_halfone, color_one)
	out_canvas = paint_points(out_canvas, points_halftwo, color_two)


print("----input----")
display(in_canvas)
print("\n----output----")
display(out_canvas)
