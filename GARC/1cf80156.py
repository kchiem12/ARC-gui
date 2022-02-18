from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():

	global input_canvas, output_canvas

	oxlen = rand_sample(1, closed_interval(3, 6))
	oylen = rand_sample(1, closed_interval(3, 6))
	obj = random_object(oxlen, oylen, border=True)
	output_canvas = new_canvas(oxlen, oylen)
	output_canvas = paint_objects(output_canvas, [[obj, 0, 0]])

	input_canvas = new_canvas(12, 12)
	start_position = rand_position(12 - oxlen + 1, 12 - oylen + 1, n = 1)[0]
	print(start_position)
	input_canvas = paint_objects(input_canvas, [[obj, start_position[0], start_position[1]]])

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
	
