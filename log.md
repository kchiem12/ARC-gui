## VHE

### 2021-10-08

If we assume a normal distribution of data, then we are implicitly using l2 (Euclidian) distance. 

### 2021-10-14

N/A

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

## GARC

### 2021-12-7

Since the vhe result with much deeper network doesn't seem good either, we should try something else: approach this in a program synthesis way. To do this, we first need a **domain specific language (DSL)** to describe **how to generate ARC**. Namely, we want to solve "generative ARC" first, then get to the real ARC problem. Note vhe also tried to solve "generative ARC".

Specifically, we will write an API package containing probabilistic functions that draw more pictures of ARC problems. These functions should follow the functional programming protocol, so that they can be represented in a lambda way and is easier for program synthesis. Here's a list of example functions we may want to implement:

- Canvas: `fun None : return a canvas`
- Object: `fun None : return an object`
- Rotate: `fun o : return a rotated object`
- Duplicate: `fun canvas, obj, displacement vectors` : return a new canvas with several objects drawn at position of displacement vectors
- Noise: a function that will randomly add noise values to the canvas

### 2021-12-17

Different from the vhe, if we really want to do it the right way, we would need to first randomly generate some inputs and then generate their corresponding outputs. Before with vhe, the inputs and outputs were treated as completely different problems but now we want to generate them together with a specific order: input first, output second. 

Restate our goal: to create an API package so that we can use functions inside this package to write programs that solve the ARC problem. **These programs we write need to be functional, but the implementation of the language package we write does not have to be.** The programs need to be in a functional fashion only because a lambda calculus expressible program is much easier for a model to learn. 

Ultimate Goal: ARC is a set to test human's abstraction and reasoning abilities. This API package we write should be able to describe how exactly human performs these abstraction and reasoning actions. This package we write should eventually steer to the right approach to generate ARC. It contains our understanding of this dataset. 

### 2022-02-04

Main Idea: we want to **write programs that are as simple as possible**. 

#### Constraints 

We should consider adding **constraints** into our programming language. This should simplify problems like [025d127b](./GARC/025d127b.py). The main reason why we had so long a program is that we have to write very carefully to make sure the object we are drawing will not go out of the boundary. So let's just allow drawing outside of the canvas (which is actually default behavior of `paint_objects`) When we want to restrict the function to only draw inside the canvas, we can pass to it an argument `within` specifying such behavior. If `within` is activated and we try to draw outside of the canvas, we can raise the error `ExecutionFailed` so to try to generate another sample, hopefully the new one is valid. 

Kevin's idea is more general than this, he suggests an `assert` function. Some conditions are passed into the `assert` function after each drawing. If the condition is not met, we raise the `ExecutionFailed` error. This is because when we generate the (input, output) pair, we may need the constraint, but the hope is when we train the model to give an output based on input, the program without the `assert` statement is just the solution. 

#### Simpler Functions :heavy_check_mark:

e.g. in `05269061`, we are now specifying the length of each diagonal line. However, we want to make each function call and each function itself be as simple as possible. Therefore, in this case, we actually only have to specify the color and say "draw a diagonal line of infinite length." That is also how people view such problems, we don't say "draw a green diagonal line of length 4", but we say "draw a gree diagonal line" as the line in geometric meaning with an infinite length. To achieve this, we can do:

- Define three new functions `parallel_ray(color = None)`, `vertical_ray(color = None)`, `diagonal_ray(color = None)` (We do not know whether this is necessary, will the model know ray and line are essentially the same thing?)

- Use the existed functions. Currently, when the length is not specified, we make it random. However, now we make it infinite when not specified, so `parallel_line(l = infinity, color = None)`, `vertical_line(l = infinity, color = None)`, `diagonal_line(l = infinity, color = None)`. This should be good because this random length feature has never been used. 
  
  Problem: When we want to draw for example a green ray, we will have to write `vertical_line(c = Green)`, while previously we don't have to write the `c=` part. Will this confuse the model if we sometimes have `vertical_line(5, Green)`, sometimes have `vertical_line(c = Green)`, and other times have `vertical_line(5)`? A solution is to write `l=` and `c=` all the time, so `vertical_line(l = 5, c = Green)`

Went with the first because it's easier to switch to other options later in this way. 

#### Coordinate System :heavy_check_mark:

The idea of `dir` specifying which quadrant to draw the object isn't too smart. We should just use the old way of `(x,y)` specifying which block to draw. (Before we are treating `(x,y)` as an origin point and use `dir` to specify which quadrant we want to draw in)

## Parser - A*

### 2022-02-18

We now shift gears to build a parser, in fact an inverse parser that reads a json input of ARC problem and outputs what commands could be used to generate this problem. We once said that solving ARC is just **find objects -> move the objects**. And this is the "**find object**" part and is also the hardest part of the problem. We hope that the GARC problem we worked on could provide us with some insight. 

In implementation, this "parser" is actually an A\* program, which searches in the program space for the commands that reproduce the problem. To build this A\*, we will need a data structure that holds the commands. A state in A\* is just a list of commands. The distance of a state to final state is the number of different pixels between the canvas our command draws and the original canvas. We also want our result to have as few commands as possible (If you can parse something into a single rectangle, don't parse it into 3 lines)

#### 2022-03-04

The result is very good. Now there are two things to do:

1. Make it run faster by using precomputation and `np.array`: we will precompute two arrays: mask - $B \times H \times W$ and a bitmap $B \times H \times W$. Each entry in these two arrays represent the result of drawing one object: `(line, length, x, y, c)` or `(rec, xlength, ylength, x, y, c)`. $B$ is the branching factor, counting how many possible combinations there are for all kinds of `object_type, length, x, y, c`. We will also have a corresponding list of length $B$, specifying what objects were drawn when we draw some pixels according to bitmap and mask. Therefore, when we run the program, it will now iterate through this list/array of length $B$, because it simply includes all the possible object combination we can have, instead of having 5 or 6 for loops of `for type, for l, for x, for y, for c, ...`
1. We will now search for a set of possible commands that can give us this result, not a single one. 
   - Think of our interpreter as encoding ways of reproducing an ARC problem into an FSM. This FSM takes in an action sequence that if executed, will reproduce the input canvas. A state in this FSM used to be an action sequence, but now we want the path to be action sequence and the **state be simply the canvas the path so far taken can draw**. Therefore, if two action sequences draw the same canvas, they are the same state. 
   - Note there are well possible to have **multiple ways** and therefore multiple paths that lead to the accept state. We want to find all of them. It's impossible to find all, but we can definitely find some by **timing out**: run the program for x seconds and then force it to terminate. 
   - Eventually we will run A* on multiple inputs and get multiple FSM, intersect all these FSM we get (there is a nice algo allows this) and that will be the interpretation of the whole problem we eventually have. 
1. It is a good idea to have a random bitmap that takes care of everything left and costs very high so we don't use it often. 