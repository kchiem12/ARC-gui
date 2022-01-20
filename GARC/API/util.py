import random
import numpy as np

def rand_bool(prob):
	"""
	Returns True with probability `prob` (0~1)
	"""
	prob = 0.5 if prob == None else prob
	return random.choices([True, False], [prob, 1 - prob])[0]
	# return True if random.randint(0,1) else False

def rotate_90(arr, n):
	"""
	Returns the object `arr` rotated by 90 degrees for `n` times
	"""
	if n > 0: return rotate_90(np.rot90(arr), n-1)
	elif n == 0: return arr
	else: raise "negative rotation times"

def map_list(fun, lst):
	return list(map(fun, lst))