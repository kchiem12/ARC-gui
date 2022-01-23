import enum
import random
 
# # creating enumerations using class
# class Color(enum.Enum):
class Color():
	Black = 0
	Cobalt = 1
	Red = 2
	Green = 3
	Yellow = 4
	Gray = 5
	Purple = 6
	Orange = 7
	Sky = 8
	Brown = 9


non_black_colors = [i+1 for i in range(9)]



def rand_color():
	return random.choice(non_black_colors)