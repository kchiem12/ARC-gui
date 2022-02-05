## Task Template

Every task should follow the instructions and naming conventions given in [`template.py`](template.py). More than a template, it should be taken as an interface. 


## Coordinate System

Coordinate starts from the lower left of the plane: 

(0, m) ------------- (n, m)
|                       |
|                       |
|                       |
|                       |
|                       |
(0, 0) ------------- (n, 0)


## Calling Convention

- When specify a color, use `Color.<color_name>` as specified in [`color.py`](API/color.py). For example, if want to use cobalt blue, don't use `1`. Instead, use `Color.Cobalt`

- When to use `rand_division(1, n, l)` and when to use `rand_sample(n, l)`?
  These two functions both return `n` random elements from list `l`, but `rand_division` returns a sorted list, while `rand_sample` returns an unsorted one. 
