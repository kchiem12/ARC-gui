import os
import numpy as np
import json
import torch
from torch.utils.data import Dataset, DataLoader
import random

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

        def pad_around_aux(p):
            """
            returns the picture p padded to a square of len max_len
            og p is at the center of padded version of p
            """
            arr = np.array(p)
            height = len(arr)
            width = len(arr[0])
            padded = np.zeros((self.max_len, self.max_len)) # 0 is black
            height_offset = (self.max_len - height) // 2
            width_offset = (self.max_len - width) // 2
            padded[height_offset : height_offset + height,
                    width_offset : width_offset + width] = arr
            padded = np.array(padded, dtype=np.intc)
            return padded # np.resize(padded, (1, self.max_len, self.max_len))

        cnt = 0
        for filename in filenames:

            if cnt > 50: break # only use a small number of data just to make sure our model is working

            f = open(data_dir + filename)
            j = json.load(f)
            datas = j["train"] if train else j["test"]

            processed = []
            self.tasks.append(filename + " in")
            self.tasks.append(filename + " out")
            for data in datas:
                d_in = data["input"]; d_out = data["output"]
                # pad around the input and flat them into a 1D vector
                padded_in = np.resize(pad_around_aux(d_in), self.size)
                padded_out = np.resize(pad_around_aux(d_out), self.size)
                processed.append({"pixel" : padded_in, "task": cnt})
                processed.append({"pixel" : padded_out, "task": cnt+1})

                # data augmentation
                for i in range(AUGMENT_TIMES):
                    # random shuffle all colors except black
                    one_to_nine = list(range(1,10))
                    new_color_map = dict(zip((one_to_nine), random.sample(one_to_nine, len(one_to_nine))))
                    new_color_map[0] = 0
                    shuffled_in = np.array(list(map(lambda x: new_color_map[x], padded_in)))
                    shuffled_out = np.array(list(map(lambda x: new_color_map[x], padded_out)))
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