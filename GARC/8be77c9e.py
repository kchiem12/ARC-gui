from API.canvas import *
from API.object import *
from API.color import *
from API.exception import *

input_canvas = None
output_canvas = None

def generate_problem():
    """
    Mirrors the input canvas over the horizontal axis
    """
    global input_canvas, output_canvas

    input_canvas = new_canvas(3, 3)
    obj = random_object(3, 3, Color.Cobalt)
    input_canvas = paint_objects(input_canvas, [(obj, 0, 0, 0)])

    output_canvas = new_canvas(3, 6)
    output_canvas = paint_objects(output_canvas, 
                                  [(obj, 0, 3, 0), 
                                   (flip_y(obj), 0, 0, 0)])
    

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
	