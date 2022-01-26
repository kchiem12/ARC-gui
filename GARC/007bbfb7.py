from API.canvas import *
from API.object import *
from API.color import *


in_canvas = new_canvas(3, 3)
in_pos = rand_position(in_canvas)
color = rand_color()
in_canvas = paint_points(in_canvas, in_pos, color)
display(in_canvas)


out_canvas = new_canvas(9, 9)
out_obj = list(map(lambda x : (in_canvas, 3 * x[0], 3 * x[1], 0), in_pos))
out_canvas = paint_objects(out_canvas, out_obj)
display(out_canvas)
