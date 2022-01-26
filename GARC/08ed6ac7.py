from doctest import OutputChecker
from API.canvas import *
from API.object import *
from API.color import *

output_canvas = new_canvas(9, 9)

heights = rand_division(1, 4, 9)
heights = list(map(lambda x : x+1, heights))
x_coors = rand_sample(4, 4)
x_coors = list(map(lambda x : 2*x+1, x_coors))

# Paint the columns in ascending order of height:
output_canvas = paint_objects(output_canvas,
							  [[vertical_line(heights[0], Color.Yellow), x_coors[0], 0, 0],
							   [vertical_line(heights[1], Color.Green), x_coors[1], 0, 0],
							   [vertical_line(heights[2], Color.Red), x_coors[2], 0, 0],
							   [vertical_line(heights[3], Color.Cobalt), x_coors[3], 0, 0]])

input_canvas = new_canvas(9, 9)
input_canvas = paint_objects(input_canvas,
							  [[vertical_line(heights[0], Color.Gray), x_coors[0], 0, 0],
							   [vertical_line(heights[1], Color.Gray), x_coors[1], 0, 0],
							   [vertical_line(heights[2], Color.Gray), x_coors[2], 0, 0],
							   [vertical_line(heights[3], Color.Gray), x_coors[3], 0, 0]])

print("----input----")
display(input_canvas)
print("----output----")
display(output_canvas)