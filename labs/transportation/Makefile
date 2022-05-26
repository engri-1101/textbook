MAIN = transportation
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*

all: lab

lab: $(KEY).ipynb $(DATA)
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

