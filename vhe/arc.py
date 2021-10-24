#PixelCNN:
import time
import os
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision
from torchvision import datasets, transforms, utils
from pixelcnn.utils import * 
from pixelcnn.model import * 
from PIL import Image

import json


#VHE:
from builtins import super
import random

import torch
from torch import nn, optim
from torch.distributions.normal import Normal
import math

from vhe import VHE, DataLoader, Transform
from arc_loader import ArcDataset

#######pixelcnn options #########
parser = argparse.ArgumentParser()
# data I/O
parser.add_argument('-i', '--data_dir', type=str,
					default='data', help='Location for the dataset')
parser.add_argument('-d', '--dataset', type=str,
					default='omni', help='Can be either cifar|mnist|omni')
# model
parser.add_argument('-q', '--nr_resnet', type=int, default=4,
					help='Number of residual blocks per stage of the model')
parser.add_argument('-n', '--nr_filters', type=int, default=40,
					help='Number of filters to use across the model. Higher = larger model.')
parser.add_argument('-a', '--mode', type=str, default='softmax', choices=['logistic_mix', 'softmax', 'gaussian'])
parser.add_argument('-m', '--nr_logistic_mix', type=int, default=None,
					help='Number of logistic components in the mixture. Higher = more flexible model')
parser.add_argument('-sm', '--nr_softmax_bins', type=int, default=2,
					help='Number of softmax bins (use instead of nr_logistic_mix)')
parser.add_argument('-l', '--lr', type=float,
					default=0.0002, help='Base learning rate')
parser.add_argument('-e', '--lr_decay', type=float, default=0.999995,
					help='Learning rate decay, applied every step of the optimization')
parser.add_argument('-b', '--batch_size', type=int, default=8, #TODO change back to 32
					help='Batch size during training per GPU')
parser.add_argument('-x', '--max_epochs', type=int,
					default=5, help='How many epochs to run in total?')
parser.add_argument('-s', '--seed', type=int, default=1,
					help='Random seed to use')
parser.add_argument('-an', '--anneal', type=int, default=None,
					help='number of epochs to anneal')
parser.add_argument('--debug', action='store_true',
					help='if the number of batches is small')
parser.add_argument('--ortho', dest='ortho_transforms', action='store_true')
parser.add_argument('--affine', action='store_true')

args = parser.parse_args()

if args.nr_logistic_mix is None and args.nr_softmax_bins is None:
	args.nr_logistic_mix = 10




# reproducibility
torch.manual_seed(args.seed)
np.random.seed(args.seed)

sample_batch_size = args.batch_size
obs = (10, 32, 32) 
rescaling	 = lambda x : (x - .5) * 2.
flip = lambda x : - x
kwargs = {'num_workers':1, 'pin_memory':True, 'drop_last':True}
loss_op = None; sample_op = None
args.mode = "logistic_mix"
assert args.mode == "logistic_mix"

if args.mode=="logistic_mix":
	loss_op   = lambda real, fake : discretized_mix_logistic_loss_1d(real, fake)
	sample_op = lambda x : sample_from_discretized_mix_logistic_1d(x, args.nr_logistic_mix)
elif args.mode=="softmax":
	loss_op   = lambda real, fake : softmax_loss_1d(real, fake)
	sample_op = lambda x : sample_from_softmax_1d(x)
elif args.mode == "gaussian":
	loss_op   = lambda real, fake: gaussian_loss(real, fake)
	sample_op = lambda x: sample_from_gaussian(x)

#######end pixelcnn options #########


# --------- real my implementation ------------
train_loader = torch.utils.data.DataLoader(ArcDataset(), batch_size=1, 
						shuffle=True, **kwargs)

test_loader = torch.utils.data.DataLoader(ArcDataset(train = False), batch_size=1, 
						shuffle=True, **kwargs)

# --------- self tuned arguments ---------------

input_channels = 10
n_inputs = 4 # size of D
input_size = 32
z_filter = 8
c_filter = 4

class Px(nn.Module):
	def __init__(self):
		super().__init__()
		self.decov = nn.ConvTranspose2d(c_filter + z_filter, input_channels, 3)
		self.x_length = input_channels * input_size * input_size
		self.localization_mu = nn.Linear(self.x_length, self.x_length)
		self.localization_sigma = nn.Linear(self.x_length, self.x_length)
		self.log_softmax = nn.LogSoftmax(dim=1)


	def forward(self, c, z, x = None):
		# c, z = B * C'H'W' 其中他们的 channel 数 C' 不相同
		c = c.reshape(-1, c_filter, 30, 30)
		z = z.reshape(-1, z_filter, 30, 30)
		cz = torch.cat((c, z), dim=1)
		# decov = (self.decov(cz)).reshape(-1, input_size, input_size, input_channels) # B * H * W * C
		# predict = torch.argmax(decov.Softmax(dim = 3), dim = 3)
		decov = (self.decov(cz)) # B*C*H*W
		pred = self.log_softmax(decov) # softmax on color dimension 
		if x is not None: # training stage
			cross_entropy = x * pred
			score = cross_entropy.sum(dim=1).sum(dim=1).sum(dim=1)
		else: # sampling / generating stage
			x = F.one_hot(torch.argmax(pred, dim=1), num_classes = input_channels)
			score = torch.zeros(sample_batch_size)

		return x, score

		
		# mu, sigma = self.localization_mu(decov), self.localization_sigma(decov)
		# sigma = sigma.exp()
		# dist = Normal(mu, sigma)
		# if x is None:
		# 	x = dist.rsample()
		# x = x.reshape(-1, self.x_length)
		# score = dist.log_prob(x).sum(dim=1)
		# x = x.reshape(-1, input_channels, input_size, input_size)
		# return x, score
		
class Qc(nn.Module):
	def __init__(self):
		super(Qc, self).__init__()
		self.kernel_size = 3
		self.stride = 1
		self.conv1 = nn.Conv2d(input_channels, c_filter, kernel_size = self.kernel_size, stride = self.stride)
		self.after1_size = (input_size - self.kernel_size + 1) // self.stride
		self.c_length = c_filter * self.after1_size* self.after1_size
		self.localization_mu = nn.Linear(self.c_length, self.c_length)
		self.localization_sigma = nn.Linear(self.c_length, self.c_length)
		
	def forward(self, inputs, c = None):
		# inputs has the shape B * D * C * H * W
		bd = inputs.reshape(-1, input_channels, input_size, input_size) # BD * C * H * W
		conved = self.conv1(bd) # BD * C' * H' * W'
		chw = conved.reshape(-1, n_inputs, c_filter * self.after1_size* self.after1_size) # B * D * C'H'W'
		pooled = torch.max(chw.permute(0,2,1), dim = 2).values # B * C'H'W'
		mu, sigma = self.localization_mu(pooled), self.localization_sigma(pooled)
		sigma = sigma.exp() # make sure sigma is positive
		dist = Normal(mu, sigma)
		if c is None:
			c = dist.rsample()
		score = dist.log_prob(c).sum(dim=1)
		return c, score
		
class Qz(nn.Module):
	def __init__(self):
		super(Qz, self).__init__()
		self.kernel_size = 3
		self.stride = 1
		self.conv1 = nn.Conv2d(input_channels, z_filter, kernel_size = self.kernel_size, stride = self.stride)
		self.after1_size = (input_size - self.kernel_size + 1) // self.stride
		self.z_length = z_filter * self.after1_size* self.after1_size
		self.localization_mu = nn.Linear(self.z_length, self.z_length)
		self.localization_sigma = nn.Linear(self.z_length, self.z_length)

	
	def forward(self, inputs, c, z = None):
		inputs = inputs.reshape(-1, input_channels, input_size, input_size) # make sure it's B * C * H * W
		conved = self.conv1(inputs)
		chw = conved.reshape(-1, self.z_length) # B * C'H'W'
		mu, sigma = self.localization_mu(chw), self.localization_sigma(chw)
		sigma = sigma.exp() # make sure sigma is positive
		dist = Normal(mu, sigma)
		if z is None:
			z = dist.rsample()
		score = dist.log_prob(z).sum(dim=1)
		return z, score
		


if __name__ == '__main__':
	vhe = VHE(encoder=[Qc(), Qz()],
		  decoder=Px())
	vhe = vhe.cuda()
	print("created vhe")
	print("number of parameters is", sum(p.numel() for p in vhe.parameters() if p.requires_grad))

	from itertools import islice

	if args.debug:
		data_cutoff = 50
		data, class_labels = zip(*islice(train_loader, data_cutoff))
	else:
		data_cutoff = None
		data, class_labels = zip(*train_loader)

	data = torch.cat(data)


	batch_size = args.batch_size

	data_loader = DataLoader(data=data, labels = {'c':class_labels, 'z':range(len(data))},
			batch_size=batch_size, k_shot= {'c': n_inputs, 'z': 1})#, transforms=[transform_small_affine, transform_ortho_affine])

	#test data:
	if data_cutoff is not None:
		test_data, test_class_labels = zip(*islice(test_loader, data_cutoff))
	else:
		test_data, test_class_labels = zip(*test_loader)
	test_data = torch.cat(test_data)
	print("test dataset size", test_data.size())

	test_data_loader = DataLoader(data=test_data, labels = {'c':test_class_labels, 'z':range(len(test_data))},
			batch_size=batch_size, k_shot= {'c': n_inputs, 'z': 1})


	# Training
	print("started training")

	optimiser = optim.Adam(vhe.parameters(), lr=1e-3)
	scheduler = lr_scheduler.StepLR(optimiser, step_size=1, gamma=args.lr_decay)

	total_iter = 0
	for epoch in range(1, args.max_epochs):

		kl_factor = min((epoch-1)/args.anneal, 1) if args.anneal else 1
		
		print("kl_factor:", kl_factor)
		batchnum = 0
		for batch in data_loader:
			# batch.inputs['c'].shape == [batch_size, n_inputs, dim_of_the_pic]
			# batch.inputs['c'].shape == [32, 2, 10, 32, 32]
			# TODO should verify whether has the same input dim as example CNN or not
			inputs = {k:v.cuda() for k,v in batch.inputs.items()}
			sizes = batch.sizes
			target = batch.target.cuda()

			optimiser.zero_grad()
			score, kl = vhe.score(inputs=inputs, sizes=sizes, x=target, return_kl=True, kl_factor=kl_factor)
			(-score).backward() 
			optimiser.step()
			batchnum += 1
			print("Batch %d Score %3.3f KLc %3.3f KLz %3.3f" % (batchnum, score.item(), kl.c.item(), kl.z.item()),flush=True)
			total_iter = total_iter + 1
		print("---Epoch %d Score %3.3f KLc %3.3f KLz %3.3f" % (epoch, score.item(), kl.c.item(), kl.z.item()))

		if epoch %5==0: 
			torch.save(vhe.state_dict(), './VHE_pixelCNN_epoch_{}.p'.format(epoch))
			print("saved model")


			#Sampling:
		for batch in islice(test_data_loader, 1):
			test_inputs = {k:v.cuda() for k,v in batch.inputs.items()}
			print("\nPosterior predictive for test inputs")
			sampled_x = vhe.sample(inputs={'c':test_inputs['c']}).x 
			sampled_result = np.array(torch.argmax(sampled_x, dim = 3), dtype = np.int32).tolist()
			# x_in = torch.tensor(test_inputs['c'])
			# x_out = torch.tensor(sampled_x)
			# x_in = np.array(torch.argmax(x_in, dim = 2), dtype = np.int32)
			# x_out = np.array(torch.argmax(x_out, dim = 1).numpy(), dtype = np.int32)
			# x_in_and_out = list(map(lambda a,b : {"input":a, "output":b}, zip(x_in,x_out)))
			x_in_and_out = list(map(lambda a : {"input":a, "output":a}, sampled_result))
			with open("samples_epoch_" + str(epoch) + ".json", 'w') as f:
				json.dump({"train":x_in_and_out}, f)

			# torchvision.utils.save_image([test_inputs['c'][i,j,:,:,:] for j in range(n_inputs) for i in range(args.batch_size)] , "sample_support_epoch_{}.png".format(epoch), padding=5, pad_value=1, nrow=args.batch_size)
			# torchvision.utils.save_image(sampled_x, "samples_epoch_{}.png".format(epoch), padding=5, pad_value=1, nrow=args.batch_size)


		#do testing
		vhe.train()

		#may not want this, but can keep:
		scheduler.step()


