MAIN = maximum_flow
LAB = $(MAIN)_lab
KEY = $(LAB)_key
IMAGES = images-lab/*
SRC = max_flow.py

all: lab

lab: $(KEY).ipynb $(IMAGES) $(SRC)
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES) $(SRC)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

