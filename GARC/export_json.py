import json
import os
import numpy as np
from API.exception import *

TASK_NAME = "1cf80156" # The name of the task to generate samples for
GEN_NUM = 10 # Number of input output pair we want to generate

input_canvases = []
output_canvases = []

task = __import__(TASK_NAME)
jsonfile = {"train": []}

for i in range(GEN_NUM):

	print("Generating Task ", i)
	
	try:
		task.generate_problem()
	except ExecutionFailed:
		continue
	
	# The way we represent our coordinate system is different from
	# system default way (See README.md)
	input_canvas = task.get_input_canvas()
	input_canvas = np.rot90(input_canvas).tolist()
	output_canvas = task.get_output_canvas()
	output_canvas = np.rot90(output_canvas).tolist()
	jsonfile["train"].append({"input": input_canvas, "output": output_canvas})

print("Generate %d %s tasks, %d successful, %d failed" %(GEN_NUM, TASK_NAME, len(jsonfile["train"]), GEN_NUM - len(jsonfile["train"])))

current_path = os.getcwd()
GARC_path = current_path if current_path[-4:] == "GARC" else current_path + "/GARC"
with open(GARC_path + "/samples/" + TASK_NAME + ".json", 'w') as f:
	json.dump(jsonfile, f)

