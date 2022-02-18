import random
import numpy as np
from API.exception import *

def rand_bool(prob = None):
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

def rand_division(n = 1, m = 1, l = 1, min_dis = 1, max_dis = 100000):
	"""
	Divide number `l` into 1~`n` divisions, each division contains `m` numbers

	Parameters
	----------
	n : int, optional
		Max number of division we want, final number of divisions will be drawn 
		uniformly from [1,n], by default 1
	m : int, optional
		Number of numbers in each division, by default 1
	l : int, optional
		Number to divide, by default 1
	min_dis: int, optional
		Minimum distance required between the first and the last point in the span,
		by default 1. Distance is defined as last point position - first point 
		position. e.g. last point is at 5, first point is at 2, their distance 
		is 5 - 2 = 3. If we are asking not for a span, but for a flat list, 
		it specifies the min distance required between each point in the list. 
	max_dis: int, optional
		Maximum distance required, by default 100000. See `min_dis` for more 
		detailed explanation

	Returns
	-------
	Case1 `n`==1 or `m`==1: [x1, x2, ...]
		A sorted list of `n` * `m` numbers randomly drawn from range `l`
	Case2 otherwise: [(x11, x12, ...), (x21, x22, ...), ... ]
		A list of n' tuples, where n' is a random number from [1, `n`]
		Each tuple represents a division. Each division has `m` numbers
		xij (i <= n', j <= m) represents the jth number in division i
		The list is sorted: x11 < x12 < ... < x21 < x22 < ...

	Raises
	------
	ExecutionFailed if l < n*m: there are not enough elements to divide
	ExecutionFailed if cannot generate a valid division within MAX_TRY times
	"""

	MAX_TRY = 50
	flat = n == 1 or m == 1
	if l < n*m: raise ExecutionFailed("No enough elements to divide")

	def helper(n, m, l):
		n = random.randint(1, n)
		# print("n %d, m %d" %(n, m))
		pool = [i for i in range(l)]
		random.shuffle(pool)
		lst = sorted(pool[:n*m])
		if flat: return lst
		this_division = []
		result = []
		for i in range(n*m):
			this_division.append(lst[i])
			if (i+1) % m == 0:
				result.append(this_division)
				this_division = []
		return result
	
	for i in range(MAX_TRY):
		valid = True
		result = helper(n, m, l)
		if flat:
			for i in range(len(result)-1):
				dis = result[i+1] - result[i]
				valid = valid and min_dis <= dis and dis <= max_dis
		else:
			for div in result:
				dis = div[-1] - div[0]
				valid = valid and min_dis <= dis and dis <= max_dis
		if valid: return result
	
	raise ExecutionFailed("Can't Generate Valid Division")

def rand_position(x, y, p=0, n=0):
	"""
	Returns a list of random (x,y) coordinates on `canvas` with either `n` mode or `p` mode

	Parameters
	----------
	p : int, optional
		The robability of each point being chosen, default 0
	n : int, optional
		The total number of positions we want to choose, default 0

	Returns
	-------
	[(x1, y1), (x2, y2), ...]
		Each (xi,yi) is a valid coordinate pair: 0 <= xi < x, 0 <= yi < y

	Raises
	------
	InvalidCommand if both `p` and `n` are specified

	"""
	if n>0 and p>0: raise InvalidCommand("Both p and n are specified, can only specify one")
	
	lst = []
	if n > 0:
		pool = [(i, j) for i in range(x) for j in range(y)]
		random.shuffle(pool)
		lst = pool[:n] # if n>1 else pool[0]
	else:
		p = p if p > 0 else random.random()
		for i in range(x):
			for j in range(y):
				if rand_bool(p): lst.append((i, j))
	return lst

def closed_interval(s, e):
	return [i for i in range(s, e+1)]

def hd(l):
	return l[0]

def tl(l):
	return l[1:] if len(l)>0 else None

def assoc(k, lst):
	"""
	Return the first found value associated with key `k` in list `lst`
	If `k` is not found, return None
	"""
	for (key, value) in lst:
		if k == key: return value
	return None

def con(x, lst):
	return lst + [x]