## ARC Development

### 2021-10-08

If we assume a normal distribution of data, then we are implicitly using l2 (Euclidian) distance. 



### 2021-10-14







### 2021-11-04

use small amount of data (high variance or high bias)

Our ARC model should be able to do 3 kinds of tasks:

- What does our model think ARC is in general?
  1. Randomly sample a $c$ from our trained prior
  1. Based on this $c$, randomly sample some new $z$, decode these $z$ to images
- What does our model think a specific problem is about?
  1. Given several training inputs (of a same class of problem), let the model learn a $c$
  1. Based on this $c$, randomly sample some $z$ and decode these $z$ to images
- Auto encode a problem
  1. Given several training inputs, (of a same class of problem), let the model learn a $c$
  1. Given a test image, encode it to a $z$
  1. Decode the $z$, try to get back the original image. 

### 2021-11-12

陈醉关于 loss 突然变为无穷的一些建议解决方法：

- gradient clipping
- snapshot
- 降低学习率
- weight decay (加个很小的1e-6)
- normalize 模型，保证 [-1,1]

### 2021-11-23

We should make the network even deeper by having 6 convolution/deconvolution layers for each encoder/decoder. Each kernel size of 2. 

### 2021-12-7

Since the vhe result with much deeper network doesn't seem good either, we should try something else: approach this in a program synthesis way. To do this, we first need a **domain specific language (DSL)** to describe **how to generate ARC**. Namely, we want to solve "generative ARC" first, then get to the real ARC problem. Note vhe also tried to solve "generative ARC".

Specifically, we will write an API package containing probabilistic functions that draw more pictures of ARC problems. These functions should follow the functional programming protocol, so that they can be represented in a lambda way and is easier for program synthesis. Here's a list of example functions we may want to implement:

- Canvas: `fun None : return a canvas`
- Object: `fun None : return an object`
- Rotate: `fun o : return a rotated object`
- Duplicate: `fun canvas, obj, displacement vectors : return a new canvas with a 

## Others



### 2021-11-04

- Check 