from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas
	
	input_canvas = new_canvas(7, 3)

	left_object = new_canvas(3, 3)
	left_points = rand_position(left_object)
	left_object = paint_points(left_object, left_points, Color.Cobalt)

	right_object = new_canvas(3, 3)
	right_points = rand_position(right_object)
	right_object = paint_points(right_object, right_points, Color.Cobalt)

	input_canvas = paint_canvas(input_canvas,
								[[left_object, 0, 0],
								 [right_object, 4, 0]])
	input_canvas = paint_objects(input_canvas, [[vertical_ray(Color.Gray), 3, 0]])
	print("----input----")
	display(input_canvas)

	output_canvas = new_canvas(3, 3)
	overlapped_points = list(filter(lambda x: x in right_points, left_points))
	output_canvas = paint_points(output_canvas, overlapped_points, Color.Red)
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
	
