MAIN = baseball_elimination
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
SRC = max_flow.py

all: lab

lab: $(KEY).ipynb $(DATA)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(SRC)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

