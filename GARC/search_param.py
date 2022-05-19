from interpreter_log import *
import argparse

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

def draw_random_alpha_theta():
	alpha_range = list(range(-10, 5, 0.1))
	log_theta_range = list(range(20, step=0.1))
	args.alpha = np.exp(random.choice(alpha_range))
	log_thetas = [random.choice(log_theta_range) for _ in range(3)]
	log_thetas.append(random.choice(range(6, step=0.1)))
	args.theta = list(map(lambda t : t - logsumexp(log_thetas), log_thetas))
	args.theta = list(np.multiply(-1, args.theta))

if args.random_search: 
	# When we randomly draw, we draw the value of alpha and the value of theta
	alpha_range = list(range(-10, 5))
	log_theta_range = list(range(20))
	args.alpha = np.exp(random.choice(alpha_range))
	log_thetas = [random.choice(log_theta_range) for _ in range(4)]
	args.theta = list(map(lambda t : t - logsumexp(log_thetas), log_thetas))
else:
	# When a user specifies, he gives value of theta and the cost of each command
	# Here for theta, we convert them to the -logP form first then normalize
	args.theta = list(np.multiply(-1, args.theta))
	args.theta = list(map(lambda t : t - logsumexp(args.theta), args.theta))

print("Alpha: ", args.alpha)
print("Theta Probabilities: ", end="")
print(["{0:0.2f}".format(t) for t in np.exp(args.theta) * 100])
# we now have the log probability, but -log probability is the cost
args.theta = list(np.multiply(-1, args.theta))
print("Theta Costs: ", end="")
print(["{0:0.2f}".format(t) for t in args.theta])
print("\n\n\n\n\n")



astar = Astar(args.alpha, args.theta)

tasks = [
	("1190e5a7", True), 
	# ("05269061", True)
]

task_cost = []
for task in tasks:
	this_task_cost = []
	for tasknum in range(3):
		# taskname, tasknum, isinput = "1190e5a7", 1, True
		(taskname, isinput) = task

		print("vvvvvvvv %s %d vvvvvvvv" %(taskname, tasknum))
		diff = astar.search_one(taskname, tasknum, isinput)
		this_task_cost.append(diff)
		astar.reset()
		print("\n\n")
	task_cost.append(this_task_cost)
	print("\n\n\n\n\n")

for task in zip(tasks, task_cost): print(task)
# search_multiple()