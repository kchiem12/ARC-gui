## `template.py` Task Template

Every task should follow the instructions and naming conventions given in [`template.py`](template.py). More than a template, it should be viewed as an interface.

## `export_json.py`

This program is used to generate a certain number of input output pairs of a particular program, and output the generated canvas in json. The json format follows the format in the original jsons given. Use argument `TASK_NAME` and `GEN_NUM` to specify which task you want to generate samples for, and how many samples you want. 

## Coordinate System

Coordinate starts from the lower left of the plane as if we are looking at the first quadrant of a plane. 

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
