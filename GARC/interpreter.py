import json
import queue
import os
import time
from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from obj_a import *

"""
Does not detect a black object.
"""


# parent_dir = os.path.dirname(os.getcwd())
# arc_data_dir = os.path.join(parent_dir, "ARCdata/data/training/")
arc_data_dir = os.path.join(os.getcwd(), "ARCdata\\data\\training\\")

def array_to_canvas(arr):
	return np.rot90(arr, 3).tolist()

def canvas_to_array(cnv):
	return np.rot90(cnv).tolist()

def read_task(taskname, index, inpt = True):
	filename = taskname + ".json"
	f = open(arc_data_dir + filename)
	j = json.load(f)
	datas = j["train"]
	data = datas[index]
	return data["input"] if inpt else data["output"]


lines = ["vertical", "parallel", "diagonal"]
recs = ["rectangle"]
types = lines + recs

def draw_object(obj):
	tp = obj.type
	x = obj.xs
	y = obj.ys
	c = obj.color
	if tp == "vertical": return [vertical_line(obj.len, c), x, y]
	if tp == "parallel": return [parallel_line(obj.len, c), x, y]
	if tp == "diagonal": return [diagonal_line(obj.len, c), x, y]
	if tp == "rectangle": return [rectangle(obj.xlen, obj.ylen, c), x, y]

def not_new(obj): return obj.type != "new"

print_frequency = 30

def Astar(canvas):
	q = queue.PriorityQueue()
	q.put(state([new_object()]))
	vis = set()
	xlen = x_length(canvas)
	ylen = y_length(canvas)
	maxlen = max(xlen, ylen)
	area = xlen * ylen

	cnt = 0
	printed_cnt = 0

	start_time = time.time()

	while not q.empty():
		s = q.get()
		# cnt += 1
		# if cnt == print_frequency:
		# 	printed_cnt += 1
		# 	cnt = 0
		# 	print(printed_cnt)
		# 	print(s)
		
		if s in vis:
			continue
		vis.add(s)

		s 

		
		if s.objs[-1].type == "new":
			for tp in types:
				if tp in lines:
					for l in range(1, maxlen+1):
						for x in range(xlen):
							for y in range(ylen):
								for c in non_black_colors:
									new_list = s.objs[:-1].copy()
									next_obj = obj(tp, x, y, c, l = l)
									# test_canvas = paint_objects(s, [next_obj])
									new_list.append(next_obj)
									objs_to_draw = list(map(draw_object, list(filter(not_new, new_list))))
									test_canvas = paint_objects(new_canvas(xlen, ylen), objs_to_draw)
									comp = sum(sum(test_canvas != canvas))
									cnt += 1
									if comp == 0: return (new_list, time.time() - start_time)
									next_state = state(new_list)
									next_state.cost = comp
									q.put(next_state)
									# if cnt < print_frequency:
									# 	printed_cnt += 1
									# 	# cnt = 0
									# 	print(printed_cnt)
									# 	display(test_canvas)
									# 	print("current state is ", s)
									# 	print("next state is ", next_state)
				elif tp in recs:
					for x in range(xlen):
						for y in range(ylen):
							for xl in range(2, xlen - x + 1):
								for yl in range(2, ylen - y + 1):
									for c in non_black_colors:
										new_list = s.objs[:-1].copy()
										next_obj = obj(tp, x, y, c, xlen = xl, ylen = yl)
										new_list.append(next_obj)
										objs_to_draw = list(map(draw_object, list(filter(not_new, new_list))))
										test_canvas = paint_objects(new_canvas(xlen, ylen), objs_to_draw)
										comp = sum(sum(test_canvas != canvas))
										cnt += 1
										if comp == 0: return (new_list, time.time() - start_time)
										next_state = state(new_list)
										next_state.cost = comp
										q.put(next_state)
										# if cnt < print_frequency:
										# 	printed_cnt += 1
										# 	# cnt = 0
										# 	print(printed_cnt)
										# 	display(test_canvas)
										# 	print("current state is ", s)
										# 	print("next state is ", next_state)

		else:
			new_list = s.objs
			new_list.append(obj("new"))
			next_state = state(new_list)
			next_state.cost = s.cost + area / 2 # 100 for adding a new object
			q.put(next_state)

if __name__ == "__main__":
	# test for parallel and vertical line
	canvas = np.array(([5,5,5], [0,0,3], [0,0,3]))
	# test for diagonal line
	canvas = np.array([[0,0,1],[0,1,0],[1,0,0]])
	# test for square
	canvas = np.array([[0,1,1],[0,1,1],[1,0,0]])

	# canvas = np.array(read_task("1190e5a7", 1, True))

	canvas = array_to_canvas(canvas)
	display(canvas)
	res = Astar(canvas)
	print(res)