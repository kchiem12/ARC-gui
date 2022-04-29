class state():
	def __init__(self, canvas = [], cost = 0, command_cost = 0, parent = None, edge = None):
		self.canvas = canvas
		self.cost = cost
		self.command_cost = command_cost
		self.parent = parent
		self.edge = edge
	
	def __hash__(self):
		return hash(tuple(map(tuple, self.canvas)))

	def __lt__(self, obj):
		"""self < obj."""
		return self.cost < obj.cost

	def __le__(self, obj):
		"""self <= obj."""
		return self.cost <= obj.cost
	
	def __str__(self):
		s = ""
		for o in self.canvas:
			s += o.__str__() + '\n'
		return s




class obj():
	def __init__(self, tp = "", xs = 0, ys = 0, color = 0, l = 0, xlen = 0, ylen = 0):
		self.type = tp
		self.len = l
		self.xlen = xlen
		self.ylen = ylen
		self.xs = xs
		self.ys = ys
		self.color = color
	
	def __hash__(self):
		return hash((self.type, self.len, self.xlen, self.ylen, self.xs, self.ys, self.color))

	def __str__(self):
		general = str.format(" at ({0}, {1}) of color {2}", self.xs, self.ys, self.color)
		if self.type == "dot": return "dot" + general
		if self.type == "vertical": return "vertical line of length " + str(self.len) + general
		if self.type == "parallel": return "parallel line of length " + str(self.len) + general
		if self.type == "diagonal": return "diagonal line of length " + str(self.len) + general
		if self.type == "rectangle": return "rectangle of xlength " + str(self.xlen) + " ylength " + str(self.ylen) + general
		if self.type == "new": return "a new object"
		if self.type == "cheat": return "bitmap of xlength " + str(self.xlen) + " ylength " + str(self.ylen) + general

	def __repr__(self):
		return self.__str__()

def _line_at(l, x, y, c):
	o = obj()
	o.len = l
	o.xs = x
	o.ys = y
	o.color = c
	return o

def vertical_line_at(l, x, y, c):
	o = _line_at(l, x, y, c)
	o.type = "vertical"
	return o

def parallel_line_at(l, x, y, c):
	o = _line_at(l, x, y, c)
	o.type = "parallel"
	return o

def diagonal_line_at(l, x, y, c):
	o = _line_at(l, x, y, c)
	o.type = "diagonal"
	return o

def new_object():
	o = obj()
	o.type = "new"
	return o