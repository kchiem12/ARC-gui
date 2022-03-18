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

# functions to create the objects
def rectangle(xlen, ylen, x, y, xl, yl, c):
	obj_canvas = np.zeros((xlen, ylen), dtype = int)
	mask_canvas = np.array(obj_canvas, dtype = bool)
	obj = np.full((xl,yl), c, dtype=int)
	mask = np.array(obj, dtype = bool)
	obj_canvas[x:x+xl, y:y+yl] = obj
	mask_canvas[x:x+xl, y:y+yl] = mask
	return obj_canvas, mask_canvas

def vertical_line(xlen, ylen, x, y, l, c):
	obj_canvas = np.zeros((xlen, ylen), dtype = int)
	mask_canvas = np.array(obj_canvas, dtype = bool)
	obj = np.full((1,l), c, dtype = int)
	mask = np.array(obj, dtype = bool)
	obj_canvas[x:x+1, y:y+l] = obj
	mask_canvas[x:x+1, y:y+l] = mask
	return obj_canvas, mask_canvas

def parallel_line(xlen, ylen, x, y, l, c):
	obj_canvas = np.zeros((xlen, ylen), dtype = int)
	mask_canvas = np.array(obj_canvas, dtype = bool)
	obj = np.full((l,1), c, dtype = int)
	mask = np.array(obj, dtype = bool)
	obj_canvas[x:x+l, y:y+1] = obj
	mask_canvas[x:x+l, y:y+1] = mask
	return obj_canvas, mask_canvas

def diagonal_line(xlen, ylen, x, y, l, c):
	obj_canvas = np.zeros((xlen, ylen), dtype = int)
	mask_canvas = np.array(obj_canvas, dtype = bool)
	for i in range(l):
		obj_canvas[x+i][y+i] = c
		mask_canvas[x+i][y+i] = True
	return obj_canvas, mask_canvas

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

	new_object_cost = 0 # user-defined new object cost
	cheating_cost = area # user-defined all cover cost
	def diff_to_target(canvas): return sum(sum(canvas != target))

	start_canvas = new_canvas(xlen, ylen)
	start_cost = diff_to_target(start_canvas)
	start_state = state(start_canvas, start_cost)
	nodes[hash(start_state)] = [start_state.canvas, []]
	q.put(start_state)

	objs = [] # a list of all possible objects to be drawn
	commands = [] # a list of the corresponding commands to generate those objects
	masks = []


	# Preprocess possible objects to draw
	for tp in types:
		if tp in lines:
			for l in range(1, maxlen+1):
				for x in range(xlen):
					for y in range(ylen):
						for c in all_colors:
							this_command = obj(tp, x, y, c, l = l)
							if tp == "vertical":
								if l > ylen - y: continue
								this_obj, this_mask = vertical_line(xlen, ylen, x, y, l, c)
							elif tp == "parallel":
								if l > xlen - x: continue
								this_obj, this_mask = parallel_line(xlen, ylen, x, y, l, c)
							elif tp == "diagonal":
								if l > xlen - x or l > ylen - y: continue
								this_obj, this_mask = diagonal_line(xlen, ylen, x, y, l, c)
							masks.append(this_mask)
							objs.append(this_obj)
							commands.append(this_command)
		elif tp in recs:
			for x in range(xlen):
				for y in range(ylen):
					for xl in range(1, xlen - x + 1):
						for yl in range(1, ylen - y + 1):
							for c in all_colors:
								# rectangle will always be inside the boundary since for loop checks for it
								this_command = obj(tp, x, y, c, xlen = xl, ylen = yl)
								this_obj, this_mask = rectangle(xlen, ylen, x, y, xl, yl, c)
								masks.append(this_mask)
								objs.append(this_obj)
								commands.append(this_command)


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

		# print("iterating new state with cost " + str(this_state.cost))
		# display(this_state.canvas)
		
		if this_hash in vis:
			continue
		vis.add(this_hash)
		this_canvas = nodes[this_hash][0]
		prev_command_cost = this_state.cost - diff_to_target(this_canvas)

		# if previous_state != None:
		# 	print(edges[(hash(previous_state), this_hash)])

		if this_hash == inter_hash:
			print("FOUND IMPORTANT INTER STATE")
			print(this_state.cost, prev_command_cost, diff_to_target(this_canvas))

		# Search Regular Objects
		next_canvases = np.where(masks, objs, this_canvas)
		for i in range(len(next_canvases)):
			next_canvas = next_canvases[i]
			# TODO: only considers the commands that improve the cost
			if diff_to_target(next_canvas) >= this_state.cost: continue

			next_hash = hash_canvas(next_canvas)
			if next_hash not in nodes: 
				nodes[next_hash] = [next_canvas, [this_hash]]
			else:
				nodes[next_hash][1].append(this_hash)
			
			# if next_hash == inter_hash:
			# 	print("MIGHT BE BECAUSE OF HERE??")

			next_cost = prev_command_cost + diff_to_target(next_canvas) + new_object_cost
			next_state = state(next_canvas, next_cost)
			
			if (this_hash, next_hash) not in edges:
				edges[(this_hash, next_hash)] = [(commands[i], next_cost)]
			else:
				edges[(this_hash, next_hash)].append((commands[i], next_cost))

			if next_cost == new_object_cost: 
				print("FOUND")
				return time.time() - start_time

			if hash(next_state) not in vis: q.put(next_state)

		# Search Cheating yet Expensive Shortcuts
		diff_canvas = np.where(this_canvas != target, target, Color.Black)
		for c in non_black_colors:
			next_canvas_to_paint = np.where(diff_canvas == c, diff_canvas, Color.Black)
			next_canvas = paint_canvas(this_canvas.copy(), [[next_canvas_to_paint, 0, 0, 0]])
			
			# TODO: only considers the commands that improve the cost
			if diff_to_target(next_canvas) >= this_state.cost: continue

			next_hash = hash_canvas(next_canvas)
			if next_hash not in nodes: 
				nodes[next_hash] = [next_canvas, [this_hash]]
			else:
				nodes[next_hash][1].append(this_hash)
			
			next_cost = prev_command_cost + diff_to_target(next_canvas) + cheating_cost
			next_state = state(next_canvas, next_cost)

			# if next_hash == inter_hash:
			# 	print("FOUND IMPORTANT INTER STATE iN NEXT")
			# 	print(next_cost, prev_command_cost, diff_to_target(next_canvas), cheating_cost)

			if (this_hash, next_hash) not in edges:
				edges[(this_hash, next_hash)] = [(obj(tp="cheat", color=c), next_cost)]
			else:
				edges[(this_hash, next_hash)].append((obj(tp="cheat", color=c), next_cost))

			if next_cost == cheating_cost: 
				print("FOUND")
				return time.time() - start_time

			if hash(next_state) not in vis: q.put(next_state)

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
		print(list(edges[(prev, current)]))
		current = prev
		display(c)
		
	return path
	
inter_state = np.array([[0,0,1,5,0,0,0],
						[1,1,1,5,1,0,1],
						[1,1,1,5,1,0,1]])
inter_state = array_to_canvas(inter_state)
inter_hash = hash_canvas(inter_state)

if __name__ == "__main__":
	# test for parallel and vertical line
	canvas = np.array(([5,5,5], [0,0,3], [0,0,3]))
	# test for diagonal line
	# canvas = np.array([[0,0,1],[0,1,0],[1,0,0]])
	# test for square
	# canvas = np.array([[0,1,1],[0,1,1],[1,0,0]])

	# 切方块
	canvas = np.array(read_task("1190e5a7", 1, True))
	# 画斜线
	# canvas = np.array(read_task("05269061", 1, True))
	# Rand Object
	# canvas = np.array(read_task("0520fde7", 2, True))

	canvas = array_to_canvas(canvas)
	display(canvas)
	print(Astar(canvas))
	print_path(canvas)
	