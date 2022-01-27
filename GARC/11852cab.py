from email.errors import MissingHeaderBodySeparatorDefect
from API.canvas import *
from API.object import *
from API.color import *

# Defining the Object
object_canvas = new_canvas(5, 5)

points0 = [(2,2)]
points1 = [(1,3), (1,1), (3,1), (3,3)]
points2 = [(2,4), (2,0), (0,2), (4,2)]
points3 = [(0,4), (4,0), (0,0), (4,4)]

c0 = rand_color()
c1 = rand_color()
c2 = rand_color()
c3 = rand_color()

# Drawing the Output Object
output_object = paint_points(object_canvas, points0, c0)
output_object = paint_points(output_object, points1, c1)
output_object = paint_points(output_object, points2, c2)
output_object = paint_points(output_object, points3, c3)

# Drawing the Input Object
#TODO: this could really just be done with 
# layers = [points1, points2, points3]
# layers[missed_point_belongs_to] = tl(layers[missed_point_belongs_to])
# But the second line does not follow the FP principle
missed_point_belongs_to = rand_sample(1, 3) + 1
print("missing layer ", missed_point_belongs_to)
if missed_point_belongs_to == 1:
	points1 = [hd(points1)]
elif missed_point_belongs_to == 2:
	points2 = [hd(points2)]
elif missed_point_belongs_to == 3:
	points3 = [hd(points3)]

input_object = paint_points(object_canvas, points0, c0)
input_object = paint_points(input_object, points1, c1)
input_object = paint_points(input_object, points2, c2)
input_object = paint_points(input_object, points3, c3)


# Defining and Drawing the Canvas
left_margin = rand_sample(1, 3) + 1
right_margin = rand_sample(1, 3) + 1
upper_margin = rand_sample(1, 3) + 1
lower_margin = rand_sample(1, 3) + 1

x_len = left_margin + 5 + right_margin
y_len = upper_margin + 5 + lower_margin

input_canvas = new_canvas(x_len, y_len)
input_canvas = paint_objects(input_canvas, [[input_object, left_margin, lower_margin, 0]])
print("----input----")
display(input_canvas)

output_canvas = new_canvas(x_len, y_len)
output_canvas = paint_objects(output_canvas, [[output_object, left_margin, lower_margin, 0]])
print("----output----")
display(output_canvas)
