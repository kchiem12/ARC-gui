import os
import numpy as np
import json
import torch
from torch.utils.data import Dataset, DataLoader
import random
from math import log2

parent_dir = os.path.dirname(os.getcwd())
arc_train_dir = os.path.join(parent_dir, "ARCdata/data/training/")
AUGMENT_TIMES = 10


class ArcDataset(Dataset):

    def __init__(self, data_dir = arc_train_dir, train = True, transform = None):
        
        filenames = os.listdir(data_dir)

        self.max_len = 32 # 30 obtained at task 1f85a75f, use 2^5=32 to be careful
        self.size = self.max_len * self.max_len
        self.dataset = []
        self.transform = transform
        self.tasks = []

        def enlarged(p):
            """
            enlarge p to a square of self.max_len, 
            scale the blocks accordingly
            """
            padded_to_2power = pad_around(p)
            to_max_len = double(padded_to_2power)
            return to_max_len
        
        def pad_around(p):
            """
            returns the picture p padded to the closest floor of power of 2
            og p is at the center of padded version of p
            """
            arr = np.array(p, dtype = np.intc)
            height = len(arr)
            width = len(arr[0])
            base = log2(max(height, width))

            # if current max side is a power of 2, just pad to that length;
            # if not a power of 2, pad to the 距离最近且比它大的2的幂
            padded_len = pow(2, int(base)) \
                         if int(base) == base \
                         else pow(2, int(base) + 1)

            padded = np.zeros((padded_len, padded_len)) # 0 is black
            height_offset = (padded_len - height) // 2
            width_offset = (padded_len - width) // 2
            
            padded[height_offset : height_offset + height,
                    width_offset : width_offset + width] = arr
            padded = np.array(padded, dtype=np.intc)
            return padded
        
        def double(p):
            """
            Requires: p has a length of 2's power
            Effects: scales p to twice its original length, 
                     scales each pixel accordingly, so now each 1X1 pixel represents a 4X4 block in the new graph
            Returns: scaled version of p
            """
            og_len = len(p)
            if og_len >= self.max_len: return np.array(p, dtype=np.intc)
            
            doubled_len = og_len * 2
            doubled = np.zeros((doubled_len, doubled_len))
            for i in range(og_len):
                for j in range(og_len):
                    doubled[2*i][2*j] = p[i][j]
                    doubled[2*i + 1][2*j] = p[i][j]
                    doubled[2*i][2*j + 1] = p[i][j]
                    doubled[2*i + 1][2*j + 1] = p[i][j]
            
            return double(doubled)

        def transform(p, trans):
            """
            trans = (t, r) 
            if t == 1, transpose problem p
            if r == 1, rotate p by 90 degree; r == 2 rotate by 180 degree; r == 3 rotate by 270 degree
            return transfomed problem p
            """
            t, r = trans
            transformed = p.T if t else p
            if r == 0: return transformed
            transformed = np.rot90(transformed)
            if r == 1: return transformed
            transformed = np.rot90(transformed)
            if r == 2: return transformed
            transformed = np.rot90(transformed)
            if r == 3: return transformed

        cnt = 0
        for filename in filenames:

            f = open(data_dir + filename)
            j = json.load(f)
            datas = j["train"] if train else j["test"]

            processed = []
            self.tasks.append(filename + " in")
            self.tasks.append(filename + " out")
            transformation = (random.randrange(0,2), random.randrange(0,4))
            for data in datas:
                d_in = data["input"]; d_out = data["output"]
                # pad around the input, 
                # let them go through some transpose/rotate transformation,
                # and flat them into a 1D vector
                transfomed_in = transform(enlarged(d_in), transformation)
                transfomed_out = transform(enlarged(d_out), transformation)
                transfomed_in = np.resize(transfomed_in, self.size)
                transfomed_out = np.resize(transfomed_out, self.size)
                processed.append({"pixel" : transfomed_in, "task": cnt})
                processed.append({"pixel" : transfomed_out, "task": cnt+1})

                # data augmentation
                for i in range(AUGMENT_TIMES):
                    # random shuffle all colors except black
                    one_to_nine = list(range(1,10))
                    new_color_map = dict(zip((one_to_nine), random.sample(one_to_nine, len(one_to_nine))))
                    new_color_map[0] = 0
                    shuffled_in = np.array(list(map(lambda x: new_color_map[x], transfomed_in)))
                    shuffled_out = np.array(list(map(lambda x: new_color_map[x], transfomed_out)))
                    processed.append({"pixel" : shuffled_in, "task": cnt})
                    processed.append({"pixel" : shuffled_out, "task": cnt+1})
            
            cnt += 2
            assert cnt <= 802
            self.dataset = self.dataset + processed
        
        def onehot_in_2D(arr):
            onehots = []
            for i in range(10):
                onehot = np.zeros(self.size)
                onehot[arr == i] = 1
                onehot.resize((self.max_len, self.max_len))
                onehots.append(onehot)
            onehots = np.array(onehots, dtype='f')
            return onehots
        
        # 转换成 10维 onehot 表示
        self.dataset = list(map(lambda x : {"pixel": onehot_in_2D(x["pixel"]), 
                                            "task": x["task"]},
                                self.dataset))

        self.halt = True

    def get_task_name(i):
        return self.tasks[i]

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        data = self.dataset[idx]
        # sample = {'input': data["input"], 'output': data["output"]}

        # if self.transform:
        #     sample = self.transform(sample)

        return data["pixel"], data["task"]