from API.canvas import *
from API.object import *
from API.color import *

x_len = rand_sample(1, closed_interval(10, 25))
y_len = rand_sample(1, closed_interval(10, 25))

color_choices = rand_sample(2, non_black_colors)
background_color = color_choices[0]
line_color = color_choices[1]

# Choose positions of the seperators from x_len-2 because seperators can only 
# be placed in the middle, you can't place the seperators at the start or the 
# end of the canvas. After choosing the positions as if they were in the middle,
# move them actually to the middle by +1 to all the coordinates
x_sep_positions = rand_division(5, 1, x_len - 2, 2)
x_sep_positions = list(map(lambda x : x+1, x_sep_positions))
x_sep_num = len(x_sep_positions)
x_seperators = list(map(lambda pos : [vertical_line(y_len, line_color), pos, 0, 0], x_sep_positions))

y_sep_positions = rand_division(5, 1, y_len - 2, 2)
y_sep_positions = list(map(lambda x : x+1, y_sep_positions))
y_sep_num = len(y_sep_positions)
y_seperators = list(map(lambda pos : [parallel_line(x_len, line_color), 0, pos, 0], y_sep_positions))

background = rectangle(x_len, y_len, background_color)
input_canvas = paint_objects(background, x_seperators)
input_canvas = paint_objects(input_canvas, y_seperators)

output_object = rectangle(x_sep_num+1, y_sep_num+1, background_color)
output_canvas = output_object

print("----input----")
display(input_canvas)
print("----output----")
display(output_canvas)