

default: train

train:
	python arc.py | tee output.txt

clean:
	touch output.txt && rm output.txt && rm result/*.json && rm model/*.p

sample:
	python sample.py

push:
	转移 json 并且 push
