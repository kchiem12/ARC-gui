import json
import queue
import time
import os
from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from obj_a_log import *

# parent_dir = os.path.dirname(os.getcwd())
# arc_data_dir = os.path.join(os.getcwd(), "ARCdata/data/training/")
# arc_data_dir = os.path.join(os.getcwd(), "ARCdata\\data\\training\\")
arc_data_dir = "/home/ly373/ARC/ARCdata/data/training/"
RUNTIME = 600.0
WANTED_RESULTS_NUM = 120
PRINT_FREQUENCY = 100
# RUNTIME = 5.0

def array_to_canvas(arr):
	"""
	Convert np array `arr` into our API coordinate system
	"""
	return np.rot90(arr, 3)

def canvas_to_array(cnv):
	"""
	Convert `cnv` of our API coordinate system into the np array coordinate system
	"""
	return np.rot90(cnv)

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

def entropy(canvas, colors = all_colors):
	etpy = 0
	area = x_length(canvas) * y_length(canvas)
	for c in colors:
		n = sum(sum(canvas == c))
		if n == 0: continue
		p = n / area
		etpy -= p * np.log(p)
	return etpy



# node: hash_canvas -> [canvas, preds]
# where `canvas` is the np representation of the state/canvas we are in 
# `preds` is a list of hash of the predecessors of this canvas
nodes = {}
# edges: (hash_u, hash_v) -> commands
# `hash_u` and `hash_v` are hash of two canvases
# `commands` contains a list of commands that can transform canvas u into v
edges = {}

total_iterations = 0

def Astar(target):
	# q may store states with the same canvas but of different cost
	# vis only records whether a state with that canvas is visited or not, 
	# regardless of the cost that is to say, after visiting a canvas once, 
	# we don't want to visit the same canvas but with a higher cost
	# Why not just use update_priority? Python doesn't support this.
	target = np.array(target)
	q = queue.PriorityQueue()
	vis = set()
	xlen = x_length(target)
	ylen = y_length(target)
	maxlen = max(xlen, ylen)
	area = xlen * ylen

	target_colors = list(filter(
		lambda c : sum(sum(np.where(target == np.array(c), True, False))) != 0, 
		all_colors))
	target_colors_num = len(target_colors)

	line_cost = np.log(area * max(xlen, ylen) * target_colors_num)
	rec_cost = 2 * np.log(area) + np.log(target_colors_num)
	baseline_cost = rec_cost
	new_object_cost = 1 # user-defined new object cost
	cheating_cost = area # user-defined all cover cost

	final_states = []
	
	def diff_to_target(canvas): return sum(sum(canvas != target))
	def heuristic_distance(canvas):
		diff_num = diff_to_target(canvas)
		if diff_num == 0: return 0
		diff_canvas = target[canvas != target]
		diff_color_kind = len(set(diff_canvas.flatten()))
		return np.log(area * diff_color_kind * diff_num) # now
		# return diff_num * np.log(area * diff_color_kind) # kevin

	blank_canvas = new_canvas(xlen, ylen)
	start_state = state(blank_canvas)
	nodes[hash(start_state)] = [start_state.canvas, []]
	q.put(start_state)

	# Preprocess possible objects to draw
	objs = [] # a list of all possible objects to be drawn
	obj_commands = [] # a list of the corresponding commands to generate those objects
	obj_masks = []

	for tp in types:
		if tp in lines:
			for l in range(1, maxlen+1):
				for x in range(xlen):
					for y in range(ylen):
						for c in target_colors:
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
							obj_masks.append(this_mask)
							objs.append(this_obj)
							obj_commands.append(this_command)
		elif tp in recs:
			for x in range(xlen):
				for y in range(ylen):
					for xl in range(1, xlen - x + 1):
						for yl in range(1, ylen - y + 1):
							for c in target_colors:
								# rectangle will always be inside the boundary since for loop checks for it
								this_command = obj(tp, x, y, c, xlen = xl, ylen = yl)
								this_obj, this_mask = rectangle(xlen, ylen, x, y, xl, yl, c)
								obj_masks.append(this_mask)
								objs.append(this_obj)
								obj_commands.append(this_command)



	""" Preprocess possible bitmaps to draw	"""
	bitmaps = []
	bitmap_commands = []
	bitmap_masks = []
	bitmap_costs = []

	for c in target_colors:

		bitmap_mask = np.where(target == np.array(c), True, False)
		bitmap = np.where(target == np.array(c), c, Color.Black)
		
		for x in range(xlen):
			for y in range(ylen):
				for xl in range(1, xlen - x + 1):
					for yl in range(1, ylen - y + 1):
						# this_bitmap = np.zeros((xlen, ylen), dtype = int)
						this_bitmap_mask = np.full((xlen, ylen), False)
						this_command = obj("cheat", x, y, c, xlen = xl, ylen = yl)
						
						this_bitmap_mask[x:x+xl, y:y+yl] = bitmap_mask[x:x+xl, y:y+yl]
						if sum(sum(this_bitmap_mask)) == 0: continue # if there is nothing to draw for this color in this region, we just skip this region
						this_command_cost = xl * yl * entropy(bitmap[x:x+xl, y:y+yl])
						# if(c==1 and x==0 and y==0 and xl==7 and yl==3):
						# 	print("!!!")
						# 	print(entropy(bitmap[x:x+xl, y:y+yl]))
						# 	print(this_command_cost)
						
						bitmaps.append(bitmap)
						bitmap_masks.append(this_bitmap_mask)
						bitmap_commands.append(this_command)
						bitmap_costs.append(this_command_cost)


	start_time = time.time()
	counter = 0 
	# previous_state = None
	# global this_state
	# this_state = None

	while not q.empty():#  and time.time() - start_time < RUNTIME:
		
		# if time.time() - start_time > RUNTIME:
		# 	print("OUT OF TIME, TERMINATE")
		# 	return
		# previous_state = this_state
		this_state = q.get()
		this_hash = hash(this_state)

		total_iterations += 1
		counter += 1
		if counter == PRINT_FREQUENCY:
			print("iterating new state with cost %f, heuristic distance %f" %(this_state.command_cost, this_state.cost - this_state.command_cost))
			display(this_state.canvas)
			print_path_state(this_state, True)
			counter = 0
				
		if this_hash in vis:
			continue
		vis.add(this_hash)
		this_canvas = nodes[this_hash][0]
		this_command_cost = this_state.command_cost

		# if previous_state != None:
		# 	print(edges[(hash(previous_state), this_hash)])

		if this_hash == inter_hash:
			print("FOUND IMPORTANT INTER STATE")
			print(this_state.cost, this_command_cost, diff_to_target(this_canvas))

		# Search Regular Objects
		next_canvases = np.where(obj_masks, objs, this_canvas)
		for i in range(len(next_canvases)):
			next_canvas = next_canvases[i]

			# TODO: only considers the commands that improve the cost
			if diff_to_target(next_canvas) >= diff_to_target(this_canvas): continue

			next_command = obj_commands[i]
			next_hash = hash_canvas(next_canvas)
			if next_hash not in nodes: 
				nodes[next_hash] = [next_canvas, [this_canvas]]
			else:
				nodes[next_hash][1].append(this_canvas)
			
			# if next_hash == inter_hash:
			# 	print("MIGHT BE BECAUSE OF HERE??")

			hrstc_dis = heuristic_distance(next_canvas)
			next_command_cost = this_command_cost + \
								(rec_cost if next_command.type == "rectangle" else line_cost)
			next_cost = next_command_cost + hrstc_dis
			next_state = state(next_canvas, next_cost, next_command_cost, this_state, next_command)
			
			if (this_hash, next_hash) not in edges:
				edges[(this_hash, next_hash)] = [(next_command, next_cost, hrstc_dis)]
			else:
				edges[(this_hash, next_hash)].append((next_command, next_cost, hrstc_dis))

			# if hrstc_dis == 0: 
			# 	print("FOUND")
			# 	return time.time() - start_time, next_state
			if hrstc_dis == 0: 
				final_states.append(next_state)
				print("FOUND")
				if len(final_states) == WANTED_RESULTS_NUM: return final_states

			if hash(next_state) not in vis: q.put(next_state)

		# Search Cheating yet Expensive Shortcuts
		next_canvases = np.where(bitmap_masks, bitmaps, this_canvas)
		for i in range(len(next_canvases)):
			next_canvas = next_canvases[i]

			# TODO: only considers the commands that improve the cost
			if diff_to_target(next_canvas) >= diff_to_target(this_canvas): continue

			next_command = bitmap_commands[i]
			next_hash = hash_canvas(next_canvas)
			if next_hash not in nodes: 
				nodes[next_hash] = [next_canvas, [this_canvas]]
			else:
				nodes[next_hash][1].append(this_canvas)
			
			# if next_hash == inter_hash:
			# 	print("MIGHT BE BECAUSE OF HERE??")
			
			hrstc_dis = heuristic_distance(next_canvas)
			next_command_cost = this_command_cost + bitmap_costs[i] + baseline_cost			
			next_cost = next_command_cost + hrstc_dis
			next_state = state(next_canvas, next_cost, next_command_cost, this_state, next_command)
			
			if (this_hash, next_hash) not in edges:
				edges[(this_hash, next_hash)] = [(next_command, next_cost, hrstc_dis)]
			else:
				edges[(this_hash, next_hash)].append((next_command, next_cost, hrstc_dis))

			# if hrstc_dis == 0: 
			# 	print("FOUND")
			# 	return time.time() - start_time, next_state
			if hrstc_dis == 0: 
				final_states.append(next_state)
				print("FOUND")
				if len(final_states) == WANTED_RESULTS_NUM: return final_states

			if hash(next_state) not in vis: q.put(next_state)

def print_path_canvas_hash(target):
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

def print_path_state(final_state, edge_only=False):
	xlen = x_length(final_state.canvas)
	ylen = y_length(final_state.canvas)
	blank_canvas = new_canvas(xlen, ylen)
	current = final_state
	path = []
	while hash_canvas(current.canvas) != hash_canvas(blank_canvas):
		if not edge_only: display(current.canvas)
		print(current.edge)
		current = current.parent
	display(blank_canvas)
	return path
	
def sorted_states_by_command_cost(states):
	for state in states: assert(state.command_cost == state.cost)
	return sorted(states, key = lambda x : x.cost)

inter_state = np.array([[0,0,1,5,0,0,0],
						[1,1,1,5,1,0,1],
						[1,1,1,5,1,0,1]])
inter_state = array_to_canvas(inter_state)
inter_hash = hash_canvas(inter_state)

if __name__ == "__main__":
	# test for parallel and vertical line
	# canvas = np.array(([5,5,5], [0,0,3], [0,0,3]))
	# test for diagonal line
	# canvas = np.array([[0,0,1],[0,1,0],[1,0,0]])
	# test for square
	# canvas = np.array([[0,1,1],[0,1,1],[1,0,0]])

	# 切方块
	# canvas = np.array(read_task("1190e5a7", 1, True))
	# 画斜线
	# canvas = np.array(read_task("05269061", 1, True))
	# Rand Object
	canvas = np.array(read_task("0520fde7", 0, True))

	canvas = array_to_canvas(canvas)
	display(canvas)
	# time_used, final_state = Astar(canvas)
	# print(time_used)
	# print_path_state(final_state)

	res = Astar(canvas)

	print("Used a total %d iterations" %(total_iterations))

	for i in range(len(res)):
		print("---------%d---------" %(i))
		print_path_state(res[i])
		print("---------%d---------" %(i))

	ress = sorted_states_by_command_cost(res)
	for i in range(len(ress)):
		print("---------%d---------" %(i))
		print_path_state(ress[i])
		print("---------%d---------" %(i))
	x = 1
	