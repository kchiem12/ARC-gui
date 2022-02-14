class InvalidCommand(Exception):
	"""
	Raised when function call does not satisfy requirement. 
	"""
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			return 'InvalidCommand, {0} '.format(self.message)
		else:
			return 'InvalidCommand has been raised'

class ExecutionFailed(Exception):
	"""
	Raised when we cannot perform this execution
	"""
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			return 'ExecutionFailed, {0} '.format(self.message)
		else:
			return 'ExecutionFailed has been raised'

class CanvasNotInitiated(Exception):
	"""
	Raised when json exporter tries to access a canvas before it is initiated
	"""
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			return 'CanvasNotInitiated, {0} '.format(self.message)
		else:
			return 'Canvas is Not Initiated'