clean:
	rm *.err && rm *.out && rm search.stats

derror:
	rm *.err

job:
	sbatch --requeue run-search.sub 1.0

search-alpha:
	bash search-alpha.sh