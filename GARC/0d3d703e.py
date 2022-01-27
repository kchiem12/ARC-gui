from matplotlib.pyplot import colormaps
from API.canvas import *
from API.object import *
from API.color import *

colors = [1,2,3,4,5,6,8,9]

input_colors = rand_sample(3, colors)
input_canvas = new_canvas(3, 3)
input_canvas = paint_objects(input_canvas, 
							 [[vertical_line(3, input_colors[0]), 0, 0, 0],
							  [vertical_line(3, input_colors[1]), 1, 0, 0],
							  [vertical_line(3, input_colors[2]), 2, 0, 0]])
print("----input----")
display(input_canvas)

def color_map(c):
	if c == 1: return 5
	elif c == 2: return 6
	elif c == 3: return 4
	elif c == 4: return 3
	elif c == 5: return 1
	elif c == 6: return 2
	elif c == 8: return 9
	elif c == 9: return 8

output_colors = list(map(color_map, input_colors))
output_canvas = new_canvas(3, 3)
output_canvas = paint_objects(output_canvas, 
							 [[vertical_line(3, output_colors[0]), 0, 0, 0],
							  [vertical_line(3, output_colors[1]), 1, 0, 0],
							  [vertical_line(3, output_colors[2]), 2, 0, 0]])

print("----output----")
display(output_canvas)