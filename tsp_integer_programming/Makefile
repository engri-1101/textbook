MAIN = tsp_integer_programming
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES = images-lab/*

all: lab

lab: $(KEY).ipynb $(IMAGES) $(DATA)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES) $(DATA)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

