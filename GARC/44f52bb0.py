import numpy as np
from API.canvas import *
from API.object import *
from API.color import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

    """
    Determine if the input 3x3 object is symmetrical
    -return a 1x1 blue tile if it is, otherwise 1x1 orange tile
    """

    global input_canvas, output_canvas

    input_canvas = new_canvas(3,3)
    input_canvas = paint_points(input_canvas, rand_position(3, 3))

    flipped_canvas = flip_y(input_canvas)
    rotated_canvas = rotate_90(flipped_canvas, 2)
    comparison = ((input_canvas == rotated_canvas) & (input_canvas == flipped_canvas)).all() #compares if the two arrays are the same

    output_canvas = new_canvas(1, 1)

    if comparison.all(): output_canvas = paint_points(output_canvas, [(0,0)], Color.Sky)
    else: output_canvas = paint_points(output_canvas, [(0,0)], Color.Orange)


    print("----input----")
    display(input_canvas)
    print("----output----")
    display(output_canvas)

    return

def get_input_canvas():
	if input_canvas is None: raise CanvasNotInitiated()
	return input_canvas

def get_output_canvas():
	if output_canvas is None: raise CanvasNotInitiated()
	return output_canvas

if __name__ == "__main__":
	generate_problem()