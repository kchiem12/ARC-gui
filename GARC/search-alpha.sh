#!/bin/bash
alphas=(0.001 0.005 0.01 0.05 0.1 0.5 1 5 10 50)
# alphas=(0.001 0.005)

for x in "${alphas[@]}"; do 
    echo $x
    sbatch --requeue run-search.sub $x
done