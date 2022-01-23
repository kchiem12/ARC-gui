from inspect import getclosurevars
from tkinter import colorchooser

from numpy import diagonal
from API.canvas import *
from API.object import *
from API.color import *

color_choice = rand_division(1, 3, 10)
print("color choices are ", color_choice)
c1 = color_choice[0]
c2 = color_choice[1]
c3 = color_choice[2]

output_canvas = new_canvas(7, 7)
output_canvas = paint_objects(output_canvas,
							  [[diagonal_line(1, c1), 0, 6, 0], 
							   [diagonal_line(2, c2), 0, 5, 0],
							   [diagonal_line(3, c3), 0, 4, 0],
							   [diagonal_line(4, c1), 0, 3, 0],
							   [diagonal_line(5, c2), 0, 2, 0],
							   [diagonal_line(6, c3), 0, 1, 0],
							   [diagonal_line(7, c1), 0, 0, 0],
							   [diagonal_line(6, c2), 1, 0, 0],
							   [diagonal_line(5, c3), 2, 0, 0],
							   [diagonal_line(4, c1), 3, 0, 0],
							   [diagonal_line(3, c2), 4, 0, 0],
							   [diagonal_line(2, c3), 5, 0, 0],
							   [diagonal_line(1, c1), 6, 0, 0]])
display(output_canvas)

def get_x(x): return 0 if x <= 6 else x-6
def get_y(y): return 6-y if y <= 6 else 0
def get_length(l): return 7 - abs(l - 6)
def get_color(l):
	remainder = l % 3
	if remainder == 0: return c1
	elif remainder == 1: return c2
	else: return c3

# There are a toal 13 diagonal lines, randomly select 3 of them as the inputs
# Order them from the upper left - origin - lower right
input_position = rand_division(1, 3, 13)
print("position choices are ", input_position)
p1 = 0 + rand_division(1, 1, 5)[0] * 3
p2 = 1 + rand_division(1, 1, 4)[0] * 3
p3 = 2 + rand_division(1, 1, 4)[0] * 3
input_canvas = new_canvas(7, 7)
input_canvas = paint_objects(input_canvas,
							  [[diagonal_line(get_length(p1), get_color(p1)), get_x(p1), get_y(p1), 0], 
							   [diagonal_line(get_length(p2), get_color(p2)), get_x(p2), get_y(p2), 0], 
							   [diagonal_line(get_length(p3), get_color(p3)), get_x(p3), get_y(p3), 0]])
display(input_canvas)
