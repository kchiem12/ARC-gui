# ARC
An attempt to solve the [Abstraction and Reasoning Corpus](https://github.com/fchollet/ARC) using program synthesis. 

Current work is on [Generative ARC](./GARC/): building API for writing programs that can generate both input and output at the same time. The idea is that if we have a model that can learn to generate ARC programs, it should be able to solve the ARC problem easily too. 

Previously, we have tried to use [Variational Homoencoder](./vhe/) to generate new input output pair, but the result didn't meet expectation. 

One can reference [this log](./log.md) for a complete development process. 