import json
import queue
import os
import time
from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from obj_a_new import *

"""
Does not detect a black object.
"""


# parent_dir = os.path.dirname(os.getcwd())
# arc_data_dir = os.path.join(parent_dir, "ARCdata/data/training/")
arc_data_dir = os.path.join(os.getcwd(), "ARCdata\\data\\training\\")
RUNTIME = 600.0
# RUNTIME = 5.0

def array_to_canvas(arr):
	"""
	Convert np array `arr` into our API coordinate system
	"""
	return np.rot90(arr, 3).tolist()

def canvas_to_array(cnv):
	"""
	Convert `cnv` of our API coordinate system into the np array coordinate system
	"""
	return np.rot90(cnv).tolist()

def read_task(taskname, index, inpt = True):
	"""
	Return the input/output of `index`th example of `taskname`
	Returns input if `inpt` is True, returns output if it's False
	"""
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

def hash_canvas(canvas):
	return hash(tuple(map(tuple, canvas)))

# node: hash_canvas -> [canvas, preds]
# where `canvas` is the np representation of the state/canvas we are in 
# `preds` is a list of hash of the predecessors of this canvas
nodes = {}
# edges: (hash_u, hash_v) -> commands
# `hash_u` and `hash_v` are hash of two canvases
# `commands` contains a list of commands that can transform canvas u into v
edges = {}

def Astar(target):
	# q may store states with the same canvas but of different cost
	# vis only records whether a state with that canvas is visited or not, 
	# regardless of the cost that is to say, after visiting a canvas once, 
	# we don't want to visit the same canvas but with a higher cost
	# Why not just use update_priority? Python doesn't support this.
	q = queue.PriorityQueue()
	vis = set()
	xlen = x_length(target)
	ylen = y_length(target)
	maxlen = max(xlen, ylen)
	area = xlen * ylen

	new_object_cost = area # user-defined new object cost
	cheating_cost = 10 * area # user-defined all cover cost

	start = state(new_canvas(xlen, ylen))
	nodes[hash(start)] = [start.canvas, []]
	q.put(start)

	objs = [] # a list of all possible objects to be drawn
	commands = [] # a list of the corresponding commands to generate those objects


	# Preprocess possible objects to draw
	# KEN -- change the code here 
	for tp in types:
		if tp in lines:
			for l in range(1, maxlen+1):
				for x in range(xlen):
					for y in range(ylen):
						for c in non_black_colors:
							# KEN -- change the code here
							# Don't use paint_objects, use native np instead
							# You'd also need a different drawing scheme for "vertical", "parallel", "diagonal" lines
							this_obj = obj(tp, x, y, c, l = l)
							this_canvas = paint_objects(new_canvas(xlen, ylen), 
														[draw_object(this_obj)])
							objs.append(this_canvas)
							commands.append(this_obj)

		elif tp in recs:
			for x in range(xlen):
				for y in range(ylen):
					for xl in range(2, xlen - x + 1):
						for yl in range(2, ylen - y + 1):
							for c in non_black_colors:
								# KEN -- change the code here
								# Don't use paint_objects, use native np instead
								this_obj = obj(tp, x, y, c, xlen = xl, ylen = yl)
								this_canvas = paint_objects(new_canvas(xlen, ylen), 
															[draw_object(this_obj)])
								objs.append(this_canvas)
								commands.append(this_obj)
	obj_num = len(objs)


	start_time = time.time()
	# previous_state = None
	# global this_state
	# this_state = None

	while not q.empty():#  and time.time() - start_time < RUNTIME:
		
		if time.time() - start_time > RUNTIME:
			print("OUT OF TIME, TERMINATE")
			return
		# previous_state = this_state
		this_state = q.get()
		this_hash = hash(this_state)

		# print("iterating new state")
		# display(this_state.canvas)
		
		if this_hash in vis:
			continue
		vis.add(this_hash)
		this_canvas = nodes[this_hash][0]

		# if previous_state != None:
		# 	print(edges[(hash(previous_state), this_hash)])

		# Search Regular Objects
		for i in range(obj_num):
			next_canvas = this_state.canvas.copy()
			# KEN -- change this code to np
			next_canvas = paint_canvas(next_canvas, [[objs[i], 0, 0, 0]])
			next_hash = hash_canvas(next_canvas)
			if next_hash not in nodes: 
				nodes[next_hash] = [next_canvas, [this_hash]]
			else:
				nodes[next_hash][1].append(this_hash)
			
			next_cost = sum(sum(next_canvas != canvas)) + new_object_cost
			next_state = state(next_canvas, next_cost)
			
			if (this_hash, next_hash) not in edges:
				edges[(this_hash, next_hash)] = [(commands[i], next_cost)]
			else:
				edges[(this_hash, next_hash)].append((commands[i], next_cost))

			if next_cost == new_object_cost: 
				print("FOUND")
				return


			if hash(next_state) not in vis: q.put(next_state)

		# Search Cheating yet Expensive Shortcuts
		# diff_canvas = np.where(this_canvas != canvas, canvas, Color.Black)
		# for c in non_black_colors:
		# 	next_canvas_to_paint = np.where(diff_canvas == c, diff_canvas, Color.Black)
		# 	next_canvas = paint_canvas(this_canvas.copy(), [[next_canvas_to_paint, 0, 0, 0]])
		# 	next_hash = hash_canvas(next_canvas)
		# 	if next_hash not in nodes: 
		# 		nodes[next_hash] = [next_canvas, [this_hash]]
		# 	else:
		# 		nodes[next_hash][1].append(this_hash)
			
		# 	next_cost = sum(sum(next_canvas != canvas)) + cheating_cost
		# 	next_state = state(next_canvas, next_cost)

		# 	if (this_hash, next_hash) not in edges:
		# 		edges[(this_hash, next_hash)] = [(obj(tp="cheat", color=c), next_cost)]
		# 	else:
		# 		edges[(this_hash, next_hash)].append((obj(tp="cheat", color=c), next_cost))

		# 	# edges[(this_hash, next_hash)] = (obj(tp="cheat", color=c), next_cost)
		# 	if next_cost == cheating_cost: 
		# 		print("FOUND")
		# 		return

		# 	if hash(next_state) not in vis: q.put(next_state)

def print_path(target):
	"""
	Print in reverse order the first path found from a blank canvas to `target`
	"""
	start = hash_canvas(new_canvas(x_length(target), y_length(target)))
	current = hash_canvas(target)
	path = []
	while current != start:
		c, preds = nodes[current]
		path.append(c)
		prev = preds[0]
		print(edges[(prev, current)][0])
		current = prev
		display(c)
		
	return path
	
inter_state = np.array([[0,0,0,5,0,0,0],
						[0,0,0,5,0,0,0],
						[0,0,0,5,0,0,0]])
inter_state = array_to_canvas(inter_state)
inter_hash = hash_canvas(inter_state)

if __name__ == "__main__":
	# test for parallel and vertical line
	canvas = np.array(([5,5,5], [0,0,3], [0,0,3]))
	# test for diagonal line
	canvas = np.array([[0,0,1],[0,1,0],[1,0,0]])
	# test for square
	canvas = np.array([[0,1,1],[0,1,1],[1,0,0]])

	# 切方块
	# canvas = np.array(read_task("1190e5a7", 1, True))
	# 画斜线
	canvas = np.array(read_task("05269061", 1, True))
	# Rand Object
	# canvas = np.array(read_task("0520fde7", 2, True))

	# canvas = np.random.rand(5, 5)
	# canvas = np.where(canvas > 0.5, 1, 2)

	canvas = array_to_canvas(canvas)
	display(canvas)
	Astar(canvas)
	print_path(canvas)
	