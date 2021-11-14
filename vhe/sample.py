import torch
import os
from vhe import VHE #, DataLoader
from arc import Qc, Qz, Px
import numpy as np
import json


# if __name__ == '__main__':



vhe = VHE(encoder=[Qc(), Qz()],
		decoder=Px())
# vhe = vhe.cuda()
# model = TheModelClass(*args, **kwargs)
# optimizer = TheOptimizerClass(*args, **kwargs)

vhe = torch.load("./VHE_pixelCNN_epoch_15.p")

print("restored vhe")

parent_dir = os.path.dirname(os.getcwd())
arc_train_dir = os.path.join(parent_dir, "ARCdata/data/training/")
filenames = os.listdir(arc_train_dir)
name2num = {k:v for k,v in zip(filenames, range(len(filenames)))}

clist = []
def sample_task(task, is_training = "train"):
	training = is_training == "train"
	filename = task + ".json"
	c = name2num[filename]
	c = 2*c if training else 2*c + 1
	clist.append(c)

sample_task("007bbfb7", "train")

sampled_x = vhe.sample(inputs={'c':clist}).x 
sampled_result = np.array(torch.argmax(sampled_x.cpu(), dim = 3), dtype = np.int32).tolist()
x_in_and_out = list(map(lambda a : {"input":a, "output":a}, sampled_result))
with open("./results/samples_tests.json", 'w') as f:
	json.dump({"train":x_in_and_out}, f)
print(sampled_x)