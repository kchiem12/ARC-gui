from API.canvas import *
from API.object import *
from API.color import *

'''
Symmetry Task

input is a 3x3 grid with colored tiles randomly dispersed

output is a 3x6 grid, where the input grid is mirrored along the center y-axis
'''

#random color
color = rand_color()

#generating the input
in_canvas = new_canvas(3, 3)
in_position = rand_position(in_canvas)
in_canvas = paint_points(in_canvas, in_position, color)
display(in_canvas)


#generating the output
out_canvas = new_canvas(6, 3)
rotated_in = rotate_90(in_canvas, 2)
out_canvas = paint_points(out_canvas, in_position, color)
obj_list = [(rotated_in, 3, 0, 1)] #for the parameter of creating the object on canvas
out_canvas = paint_objects(out_canvas, obj_list)
display(out_canvas)


