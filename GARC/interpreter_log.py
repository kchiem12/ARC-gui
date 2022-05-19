import argparse
from functools import reduce
import json
import queue
import time
import cProfile
import os
import random
from API.canvas import *
from API.object import *
from API.color import *
from API.util import *
from obj_a_log import *
from scipy.special import loggamma, logsumexp

RUNTIME = 600.0
WANTED_RESULTS_NUM = 1000
PRINT_FREQUENCY = 100
SERVER = True
# parent_dir = os.path.dirname(os.getcwd())
arc_data_dir = "/home/ly373/ARC/ARCdata/data/training/" if SERVER \
			   else os.path.join(os.getcwd(), "ARCdata\\data\\training\\")
# RUNTIME = 5.0

parser = argparse.ArgumentParser()
# data I/O
parser.add_argument('-a', '--alpha', type = float, default = 1.0, 
					help='alpha value in Dirichlet Distribution')
parser.add_argument('-th','--theta', nargs='+', type = float,
					default = [1.0, 1.0, 1.0, 1.0],
					help='four theta value of dot, line, rectangle, and bitmap')
parser.add_argument('-r', '--random-search', action = "store_true",
					# type = bool, default = False,
					help='If set to True, ignores all hyperparameter arguments and draw them at random')

args = parser.parse_args()
if args.random_search: 
	alpha_range = list(range(-10, 5))
	log_theta_range = list(range(20))
	args.alpha = np.exp(random.choice(alpha_range))
	log_thetas = [random.choice(log_theta_range) for _ in range(4)]
	args.theta = list(map(lambda t : t - logsumexp(log_thetas), log_thetas))
else:
	args.theta = list(np.multiply(-1, args.theta))
	args.theta = list(map(lambda t : t - logsumexp(args.theta), args.theta))

print("Alpha: ", args.alpha)
print("Theta Probabilities: ", end="")
print(["{0:0.2f}".format(t) for t in np.exp(args.theta) * 100])
# we now have the log probability, but -log probability is the cost
args.theta = list(np.multiply(-1, args.theta))
print("Theta Costs: ", end="")
print(["{0:0.2f}".format(t) for t in args.theta])

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


dots = ["dot"]
lines = ["vertical", "parallel", "diagonal"]
recs = ["rectangle"]
types = dots + lines + recs

# functions to create the objects
def dot(xlen, ylen, x, y, c):
	obj_canvas = np.zeros((xlen, ylen), dtype = int)
	mask_canvas = np.array(obj_canvas, dtype = bool)
	obj_canvas[x, y] = c
	mask_canvas[x, y] = True
	return obj_canvas, mask_canvas

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


def dirchilet_multinom_cost(counts, alpha = 1):
	n = sum(counts)
	K = len(counts)
	res = loggamma(K * alpha) + loggamma(n+1) - loggamma(n + K*alpha)
	for k in range(K):
		res += loggamma(counts[k]+alpha) - loggamma(alpha) - loggamma(counts[k]+1)
	return -res


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
		non_black_colors))
	target_colors += [Color.Black] # always include black
	target_colors_num = len(target_colors)

	def norm_factor():
		# line_bitmap = dirchilet_multinom_cost([max(xlen, ylen), 0], args.alpha) + np.log(target_colors_num)
		# rec_bitmap = dirchilet_multinom_cost([area, 0], args.alpha) + np.log(target_colors_num)
		# dot_bitmap = dirchilet_multinom_cost([1, 0], args.alpha) + np.log(target_colors_num)
		# print("Calculating Bitmap Factor")
		# print("normal line " +  str(line_cost) + " | line as bitmap " + str(line_bitmap))
		# print("normal rec " +  str(rec_cost) + " | rec as bitmap " + str(rec_bitmap))
		# print("normal dot " +  str(dot_cost) + " |  dot as bitmap " + str(dot_bitmap))
		# factor = max(line_cost / line_bitmap, rec_cost / rec_bitmap, dot_cost / dot_bitmap)
		# print("Bitmap Factor is " + str(factor) +"\n")

		"不对，应该取最小的 rec line dot 而不是最大的面积，最小的面积才能有最小的dirichlet score，才能算出最大的 factor"
		dot_bitmap = dirchilet_multinom_cost([1, 0], args.alpha) + np.log(target_colors_num)
		factor = rec_cost / dot_bitmap
		print("Bitmap Factor is " + str(factor) +"\n")
		return factor

	theta_dot_cost, theta_line_cost, theta_rec_cost, theta_bm_cost = args.theta 
	dot_cost = np.log(area) + np.log(target_colors_num) + theta_dot_cost
	line_cost = np.log(area * max(xlen, ylen) * target_colors_num) + theta_line_cost
	rec_cost = 2 * np.log(area) + np.log(target_colors_num) + theta_rec_cost
	baseline_cost = 2 * np.log(area) + np.log(target_colors_num)
	bitmap_factor = 1 # * norm_factor()
	# new_object_cost = 1 # user-defined new object cost
	# cheating_cost = area # user-defined all cover cost

	""" 
	Duplicate Code with Bitmap Cost Preprocessing
	Need to Change Both sections when making changes
	"""
	def bitmap_cost(bitmap):
		bitmap = np.array(bitmap, dtype = bool)
		xl = len(canvas)
		yl = len(canvas[0])
		colored_bits = sum(sum(bitmap))
		cbitmap = dirchilet_multinom_cost([colored_bits, xl*yl - colored_bits], args.alpha) \
				+ baseline_cost + theta_bm_cost
		return cbitmap

	def get_desired_cost(prog):
		res = 0
		res += prog["dot"] * dot_cost
		res += prog["line"] * line_cost
		res += prog["rec"] * rec_cost
		res = reduce(lambda x,y : x + bitmap_cost(y), prog["bitmap"], res)
		return res
	
	desired_cost = get_desired_cost(sol.desired_program)
	final_states = []
	
	def diff_to_target(canvas): return sum(sum(canvas != target))
	def heuristic_distance(canvas):
		diff_num = diff_to_target(canvas)
		if diff_num == 0: return 0
		diff_canvas = target[canvas != target]
		diff_color_kind = len(set(diff_canvas.flatten()))
		# return np.log(area * diff_color_kind * diff_num) # now
		return diff_num * np.log(area * diff_color_kind) # kevin

	blank_canvas = new_canvas(xlen, ylen)
	start_state = state(blank_canvas)
	nodes[hash(start_state)] = [start_state.canvas, []]
	q.put(start_state)

	# Preprocess possible objects to draw
	objs = [] # a list of all possible objects to be drawn
	obj_commands = [] # a list of the corresponding commands to generate those objects
	obj_masks = []

	for tp in types:
		if tp in dots:
			for x in range(xlen):
				for y in range(ylen):
					for c in target_colors:
						this_command = obj(tp, x, y, c)
						this_obj, this_mask = dot(xlen, ylen, x, y, c)
						obj_masks.append(this_mask)
						objs.append(this_obj)
						obj_commands.append(this_command)
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
						this_bitmap_mask = np.full((xlen, ylen), False)
						this_command = obj("cheat", x, y, c, xlen = xl, ylen = yl)
						
						this_bitmap_mask[x:x+xl, y:y+yl] = bitmap_mask[x:x+xl, y:y+yl]
						if sum(sum(this_bitmap_mask)) == 0: continue # if there is nothing to draw for this color in this region, we just skip this region
						# this_command_cost = pow(xl*yl, 2.5) / area \
						# 					* (1 - sum(sum(this_bitmap_mask)) / (xl*yl))
										#   * entropy(bitmap[x:x+xl, y:y+yl])
						colored_bits = sum(sum(this_bitmap_mask))
						
						""" Duplicate Code with Bitmap Cost Preprocessing, 
							need to Change Both sections when making changes
							This section is kept for better performance. """
						this_command_cost = dirchilet_multinom_cost([colored_bits, xl*yl - colored_bits], args.alpha) + baseline_cost + theta_bm_cost
						# this_command_cost = bitmap_factor * this_command_cost
						
						bitmaps.append(bitmap)
						bitmap_masks.append(this_bitmap_mask)
						bitmap_commands.append(this_command)
						bitmap_costs.append(this_command_cost)


	""" Start to Search """
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

		global total_iterations
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
								(rec_cost if next_command.type == "rectangle" else \
								 dot_cost if next_command.type == "dot" else line_cost)
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
				if next_cost == desired_cost: print("Found Desired Program at iteration %d" %(total_iterations))
				if len(final_states) == WANTED_RESULTS_NUM: return final_states, desired_cost

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
			next_command_cost = this_command_cost + bitmap_costs[i]
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
				if next_cost == desired_cost: print("Found Desired Program at iteration %d" %(total_iterations))
				if len(final_states) == WANTED_RESULTS_NUM: return final_states, desired_cost

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
		print(current.edge, current.command_cost)
		current = current.parent
	if not edge_only: display(blank_canvas)
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

	if SERVER:
		profiler = cProfile.Profile()
		profiler.enable()

	# test for parallel and vertical line
	# canvas = np.array(([5,5,5], [0,0,3], [0,0,3]))
	# test for diagonal line
	# canvas = np.array([[0,0,1],[0,1,0],[1,0,0]])
	# test for square
	# canvas = np.array([[0,1,1],[0,1,1],[1,0,0]])

	# 切方块
	TASKNAME, TASKNUM, ISINPUT = "1190e5a7", 1, True

	# 切方块
	# canvas = np.array(read_task("1190e5a7", 0, True))
	# 画斜线
	# canvas = np.array(read_task("05269061", 1, False))
	# Rand Object
	# canvas = np.array(read_task("0520fde7", 2, True))

	# canvas = np.array(read_task("06df4c85", 2, True))

	canvas = np.array(read_task(TASKNAME, TASKNUM, ISINPUT))
	sol = __import__("p_"+TASKNAME+"_"+str(TASKNUM))

	canvas = array_to_canvas(canvas)
	display(canvas)
	# time_used, final_state = Astar(canvas)
	# print(time_used)
	# print_path_state(final_state)

	predictions, solution_cost = Astar(canvas)

	if SERVER:
		profiler.disable()
		profiler.dump_stats("/home/ly373/ARC/GARC/search.stats")
	
	print("Looking for a program with cost " + str(solution_cost))
	print("Used a total %d iterations" %(total_iterations))

	# for i in range(len(res)):
	# 	print("---------%d---------" %(i))
	# 	print_path_state(res[i])
	# 	print("---------%d---------" %(i))

	print ("!!!!!!!!!! SORTED !!!!!!!!!!")
	sorted_prediction = sorted_states_by_command_cost(predictions)
	solution_rank = -1
	for i in range(len(sorted_prediction)):
		if sorted_prediction[i].command_cost == solution_cost:
			solution_rank = i+1
	print("solution ranked at " + str(solution_rank) \
		  if solution_rank > 0 else "solution not found")
	for i in range(len(sorted_prediction)):
		print("---------%d---------" %(i))
		print_path_state(sorted_prediction[i])
		print("---------%d---------" %(i))
	