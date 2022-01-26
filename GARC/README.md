Coordinate starts from the lower left of the plane: 

(0, m) ------------- (n, m)
|                       |
|                       |
|                       |
|                       |
|                       |
(0, 0) ------------- (n, 0)


- When to use `rand_division(1, n, l)` and when to use `rand_sample(n, l)`?
  These two functions both return `n` random elements from list `l`, but `rand_division` returns a sorted list, while `rand_sample` returns an unsorted one. 
