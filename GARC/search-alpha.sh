#!/bin/bash
alphas=(0.001 0.005 0.01 0.05 0.1 0.5 1 5 10 50)
# alphas=(0.01 0.015 0.02 0.025 0.03 0.035 0.04 0.045 0.05)
# alphas=(0.001 0.005)

for x in "${alphas[@]}"; do 
    echo $x
    sbatch --requeue run-search.sub $x
done