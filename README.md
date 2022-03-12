# ARC
An attempt to solve the [Abstraction and Reasoning Corpus](https://github.com/fchollet/ARC) using program synthesis. 

Current work is on building [an interpreter](./GARC/interpreter.py) to detect objects in the problem.

Previously, we did

- [Variational Homoencoder](./vhe/) to generate new input output pair, but the result didn't meet expectation. 
- [Generative ARC](./GARC/): building API for writing programs that can generate both input and output at the same time. The idea is that if we have a model that can learn to generate ARC programs, it should be able to solve the ARC problem easily too. 

One can reference [this log](./log.md) for a complete development process. 