from interpreter_another import *
import matplotlib.pyplot as plt
import random
import numpy as np

TRY_TIMES = 10

def dimension_scalibility_test():
	x_range = range(10, 30, 2)
	ylen = 5
	def dimension_scalibility_test_once():
		time_list = []
		for xlen in x_range:
			canvas = new_canvas(xlen, ylen)
			canvas = paint_objects(canvas, [[vertical_ray(), xlen-1, 0]])
			interpretation = Astar(canvas)
			time_used = interpretation[1]
			time_list.append(time_used)
		print("Finished One Try")
		return (x_range, time_list)
		plt.plot(x_range, time_list)
		plt.savefig('dimension.png')
	result = [dimension_scalibility_test_once()[1] for _ in range(TRY_TIMES)]
	result = np.mean(result, axis=0)
	plt.plot(x_range, result)
	plt.savefig('dimensionavg.png')

def objnum_scalibility_test():
	ylen = 3
	l = 10
	def objnum_scalibility_test_once():
		time_list = []
		for obj_num in range(1, l+1):
			canvas = new_canvas(l, ylen)
			obj_list = []
			c = rand_color()
			for i in range(1, obj_num+1):
				obj_list.append([vertical_ray(c), l-i, 0])
				c = random.choice(list(filter(lambda x : x != c, non_black_colors)))
			canvas = paint_objects(canvas, obj_list)
			interpretation = Astar(canvas)
			time_used = interpretation[1]
			# print("#" , obj_num)
			# print(interpretation[0])
			time_list.append(time_used)
		print("Finished One Try")
		return (range(1, l+1), time_list)
		plt.plot(range(1, l+1), time_list)
		plt.savefig('objects2.png')
	result = [objnum_scalibility_test_once()[1] for _ in range(TRY_TIMES)]
	result = np.mean(result, axis=0)
	plt.plot(range(1, l+1), result)
	plt.savefig('objectsavg_div2.png')

def speed_test():
	canvas = np.array(read_task("1190e5a7", 1, True))
	canvas = array_to_canvas(canvas)
	result = [Astar(canvas) for _ in range(TRY_TIMES)]
	result = np.mean(result, axis=0)
	print(result)

# dimension_scalibility_test()
# objnum_scalibility_test()
speed_test()