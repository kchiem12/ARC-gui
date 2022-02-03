import random
import numpy as np

def rand_bool(prob):
	"""
	Returns True with probability `prob` (0~1)
	"""
	prob = 0.5 if prob == None else prob
	return random.choices([True, False], [prob, 1 - prob])[0]
	# return True if random.randint(0,1) else False

def rotate_90(arr, n = 1):
	"""
	Returns the object `arr` rotated by 90 degrees cw for `n` times
	"""
	n = -n % 4 # np.rot90 rotates ccw, we want to rotate cw
	return np.rot90(arr, n)
	# if n > 0: return rotate_90(np.rot90(arr), n-1)
	# elif n == 0: return arr
	# else: raise "negative rotation times"

def flip_x(arr):
	"""
	Flip the x-axis of `arr`. Equivalent to flip it wrt y-axis
	"""
	return np.flip(arr, 0)

def flip_y(arr):
	"""
	Flip the y-axis of `arr`. Equivalent to flip it wrt x-axis
	"""
	return np.flip(arr, 1)

def rand_sample(n, l, with_replacement = False):
	"""
	Returns `n` elements randomly sampled from `l`, default without replacement

	Parameters
	----------
	n : int
		number of elements to be selected
	l : list or int
		If l is a list: we sample from l,
		If l is an int: we sample from [0 - n]
	with_replacement : bool, optional
		If True, sample with replacement
		If False, sample without replacement; default is False

	Returns
	-------
	list
		sampled elements
	"""
	pool = l if type(l) == list else [i for i in range(l)]
	if with_replacement:
		return random.choices(pool, k=n)
	else:
		random.shuffle(pool)
		return pool[:n] if n>1 else pool[0]

def closed_interval(s, e):
	return [i for i in range(s, e+1)]

def hd(l):
	return l[0]

def tl(l):
	return l[1:] if len(l)>0 else None