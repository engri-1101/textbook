MAIN = redistricting
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES = images/*
SRCS = redistricting.py polyomino.py

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES) $(SRCS)
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRCS)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

