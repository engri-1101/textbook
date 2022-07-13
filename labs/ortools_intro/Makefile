MAIN = ortools_intro
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES_LAB = images-lab/*
IMAGES_KEY = images-key/*

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES_LAB)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES_LAB)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

